from __future__ import annotations

from typing import Any, Callable

import PyQt5.QtCore as QtCore


class BindingEndpoint(object):
    def __init__(
        self,
        instance: object,
        getter: Callable[..., Any],
        setter: Callable[..., Any],
        valueChangedSignal: QtCore.pyqtSignal,
    ):
        """Creates an instace of this class that contains the triplet of:
        getter, setter and change notification signal,
        as well as the object instance and it's memory id
        to which the binding triplet belongs.

        :param instance: object to obtain getter and setter from
        :param getter: property or function from object
        :param setter: setter or function from object
        :param valueChangedSignal: signal from object used to notify that the
                                   underlined property has changed
        """
        self.instance_id = id(instance)
        self.instance = instance
        self.getter = getter
        self.setter = setter
        self.valueChangedSignal = valueChangedSignal


class Observer(QtCore.QObject):
    def __init__(self, bindings: list[tuple[object, str, type]] | None = None):
        """Create an instance of this class to connect binding endpoints
        together and intiate a 2-way binding between them.

        :param bindings: list of tuples representing objects, property names
                         and signal types to bind together, defaults to None
        """
        super().__init__()
        self.bindings: dict[int, BindingEndpoint] = {}
        self.ignoreEvents = False
        if bindings:
            for instance, property_name, *types in bindings:
                self.bind_to_property(instance, property_name, types)

    def bind(
        self,
        instance: object,
        getter: Callable[..., Any],
        setter: Callable[..., Any],
        valueChangedSignal: QtCore.pyqtSignal,
        types: list[type] | None = None,
    ) -> None:
        """Creates an endpoint and call bindToEndpoint(endpoint). This is a convenience method.

        :param instance: object to obtain getter, setter and changedSignal from
        :param getter: getter of property from object
        :param setter: setter of property from object
        :param valueChangedSignal: signal from object used to notify that the
                                   underlined property has changed
        :param types: list of types to bind against signal, defaults to None
        """
        endpoint = BindingEndpoint(instance, getter, setter, valueChangedSignal)
        self.bind_to_endpoint(endpoint, types)

    def bind_to_endpoint(
        self, bindingEndpoint: BindingEndpoint, types: list[type] | None = None
    ) -> None:
        """2-way binds the target endpoint to all other registered endpoints.

        :param bindingEndpoint: binding endpoint to bind with other endpoints
        :param types: list of types to bind against signal, defaults to None
        """
        self.bindings[bindingEndpoint.instance_id] = bindingEndpoint
        if types:
            for _type in types:
                bindingEndpoint.valueChangedSignal[
                    _type
                ].connect(  # type: ignore[index]
                    self._updateEndpoints
                )
        else:
            bindingEndpoint.valueChangedSignal.connect(  # type: ignore[attr-defined]
                self._updateEndpoints
            )

    def bind_to_property(
        self, instance: object, propertyName: str, types: list[type] | None = None
    ) -> None:
        """2-way binds to an instance property according to one of the
        following naming conventions:

        @property, propertyName.setter and pyqtSignal
        - getter: propertyName
        - setter: propertyName
        - changedSignal: propertyNameChanged

        getter, setter and pyqtSignal (this is used when binding to
        standard QWidgets like QSpinBox)
        - getter: propertyName()
        - setter: setPropertyName()
        - changedSignal: propertyNameChanged

        :param instance: object to obtain getter/setter/properties from
        :param propertyName: name of property to obtain getter/setter from
        :param types: list of types to bind against signal, defaults to None
        """
        getterAttribute = getattr(instance, propertyName)

        if callable(getterAttribute):
            # the propertyName turns out to be a method
            # (like value()), assume the corresponding setter is called setValue()
            getter = getterAttribute

            if len(propertyName) > 1:
                setter = getattr(
                    instance, "set" + propertyName[0].upper() + propertyName[1:]
                )
            else:
                setter = getattr(instance, "set" + propertyName[0].upper())
        else:

            def getter() -> Any:
                return getterAttribute

            def setter(value: Any) -> None:
                setattr(instance, propertyName, value)

        valueChangedSignal = getattr(instance, propertyName + "Changed")

        self.bind(instance, getter, setter, valueChangedSignal, types)

    def _updateEndpoints(self, *args: Any, **kwargs: dict[str, Any]) -> None:
        """Updates all endpoints except the one from which this slot was called.

        Note: this method is probably not complete threadsafe.
        Maybe a lock is needed when setter self.ignoreEvents
        """
        sender = self.sender()
        if not self.ignoreEvents:
            self.ignoreEvents = True

            for binding in self.bindings.values():
                if binding.instance_id == id(sender):
                    continue

                binding.setter(*args, **kwargs)

            self.ignoreEvents = False
