from typing import Any, Callable, List, Tuple

import PyQt5.QtCore as QtCore


class BindingEndpoint(object):
    def __init__(self, instance: object, getter: Callable[[], Any], 
                 setter: Callable[[], Any], valueChangedSignal: QtCore.pyqtSignal):
        """Creates an instace of this class that contains the triplet of: getter, setter and change notification signal, 
        as well as the object instance and it's memory id to which the binding triplet belongs.

        :param instance: object to obtain getter and setter from
        :type instance: object
        :param getter: property or function from object
        :type getter: Callable[[], Any]
        :param setter: setter or function from object
        :type setter: Callable[[], Any]
        :param valueChangedSignal: signal from object used to notify that the 
                                   underlined property has changed
        :type valueChangedSignal: QtCore.pyqtSignal
        """
        self.instance_id = id(instance)
        self.instance = instance
        self.getter = getter
        self.setter = setter
        self.valueChangedSignal = valueChangedSignal


class Observer(QtCore.QObject):
    def __init__(self, bindings: List[Tuple[object, str]]=None):
        """Create an instance of this class to connect binding endpoints 
        together and intiate a 2-way binding between them.

        :param bindings: list of tuples representing objects 
                         and property names to bind together, defaults to None
        :type bindings: List[Tuple[object, str]], optional
        """
        super().__init__()
        self.bindings = {}
        self.ignoreEvents = False
        if bindings:
            for instance, property_name in bindings:
                self.bind_to_property(instance, property_name)

    def bind(self, instance: object, getter: Callable[[], Any], 
             setter: Callable[[], Any], valueChangedSignal: QtCore.pyqtSignal):
        """Creates an endpoint and call bindToEndpoint(endpoint). This is a convenience method.

        :param instance: object to obtain getter, setter and changedSignal from
        :type instance: object
        :param getter: getter of property from object
        :type getter: Callable[[], Any]
        :param setter: setter of property from object
        :type setter: Callable[[], Any]
        :param valueChangedSignal: signal from object used to notify that the 
                                   underlined property has changed
        :type valueChangedSignal: QtCore.pyqtSignal
        """
        endpoint = BindingEndpoint(instance, getter, setter, valueChangedSignal)
        self.bind_to_endpoint(endpoint)

    def bind_to_endpoint(self, bindingEndpoint: BindingEndpoint):
        """2-way binds the target endpoint to all other registered endpoints.

        :param bindingEndpoint: binding endpoint to bind with other endpoints
        :type bindingEndpoint: BindingEndpoint
        """
        self.bindings[bindingEndpoint.instance_id] = bindingEndpoint
        bindingEndpoint.valueChangedSignal.connect(self._updateEndpoints)
        
    def bind_to_property(self, instance: object, propertyName: str):
        """2-way binds to an instance property according to one of the following naming conventions:

        @property, propertyName.setter and pyqtSignal
        - getter: propertyName
        - setter: propertyName
        - changedSignal: propertyNameChanged

        getter, setter and pyqtSignal (this is used when binding to standard QWidgets like QSpinBox)
        - getter: propertyName()
        - setter: setPropertyName()
        - changedSignal: propertyNameChanged

        :param instance: object to obtain getter/setter/properties from
        :type instance: object
        :param propertyName: name of property to obtain getter/setter from
        :type propertyName: str
        """
        getterAttribute = getattr(instance, propertyName)
        if callable(getterAttribute):
            # the propertyName turns out to be a method (like value()), assume the corresponding setter is called setValue()
            getter = getterAttribute
            if len(propertyName) > 1:
                setter = getattr(instance, "set" + propertyName[0].upper() + propertyName[1:])
            else:
                setter = getattr(instance, "set" + propertyName[0].upper())
        else:
            getter = lambda: getterAttribute
            setter = lambda value: setattr(instance, propertyName, value)

        
        valueChangedSignal = getattr(instance, propertyName + "Changed")

        self.bind(instance, getter, setter, valueChangedSignal)

    def _updateEndpoints(self, *args, **kwargs):
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

                binding.setter(*args,**kwargs)

            self.ignoreEvents = False
