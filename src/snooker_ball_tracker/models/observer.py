import PyQt5.QtCore as QtCore


class BindingEndpoint(object):
    """
    Data object that contains the triplet of: getter, setter and change notification signal, 
    as well as the object instance and it's memory id to which the binding triplet belongs.
    
    Parameters:
        instance -- the object instance to which the getter, setter and changedSignal belong
        getter -- the value getter method
        setter -- the value setter method
        valueChangedSignal -- the pyqtSignal that is emitted with the value changes
    """
    def __init__(self,instance,getter,setter,valueChangedSignal):
        self.instanceId = id(instance)
        self.instance = instance
        self.getter = getter
        self.setter = setter
        self.valueChangedSignal = valueChangedSignal

        

class Observer(QtCore.QObject):
    """
    Create an instance of this class to connect binding endpoints together and intiate a 2-way binding between them.
    """
    def __init__(self, bindings=None):
        super().__init__()

        self.bindings = {}
        self.ignoreEvents = False
        if bindings:
            for instance, propertyName in bindings:
                self.bindToProperty(instance, propertyName)

    def bind(self,instance,getter,setter,valueChangedSignal):
        """
        Creates an endpoint and call bindToEndpoint(endpoint). This is a convenience method.

        Parameters:
            instance -- the object instance to which the getter, setter and changedSignal belong
            getter -- the value getter method
            setter -- the value setter method
            valueChangedSignal -- the pyqtSignal that is emitted with the value changes
        """
        endpoint = BindingEndpoint(instance,getter,setter,valueChangedSignal)
        self.bindToEndPoint(endpoint)

    def bindToEndPoint(self,bindingEndpoint):
        """
        2-way binds the target endpoint to all other registered endpoints.
        """
        self.bindings[bindingEndpoint.instanceId] = bindingEndpoint
        bindingEndpoint.valueChangedSignal.connect(self._updateEndpoints)
        
    def bindToProperty(self,instance,propertyName):
        """
        2-way binds to an instance property according to one of the following naming conventions:

        @property, propertyName.setter and pyqtSignal
        - getter: propertyName
        - setter: propertyName
        - changedSignal: propertyNameChanged

        getter, setter and pyqtSignal (this is used when binding to standard QWidgets like QSpinBox)
        - getter: propertyName()
        - setter: setPropertyName()
        - changedSignal: propertyNameChanged
        """

        getterAttribute = getattr(instance,propertyName)
        if callable(getterAttribute):
            #the propertyName turns out to be a method (like value()), assume the corresponding setter is called setValue()
            getter = getterAttribute
            if len(propertyName) > 1:
                setter = getattr(instance,"set" + propertyName[0].upper() + propertyName[1:])
            else:
                setter = getattr(instance,"set" + propertyName[0].upper())
        else:
            getter = lambda: getterAttribute
            setter = lambda value: setattr(instance,propertyName,value)

        
        valueChangedSignal = getattr(instance,propertyName + "Changed")

        self.bind(instance,getter,setter,valueChangedSignal)

    def _updateEndpoints(self,*args,**kwargs):
        """
        Updates all endpoints except the one from which this slot was called.

        Note: this method is probably not complete threadsafe. Maybe a lock is needed when setter self.ignoreEvents
        """

        sender = self.sender()
        if not self.ignoreEvents:
            self.ignoreEvents = True

            for binding in self.bindings.values():
                if binding.instanceId == id(sender):
                    continue

                binding.setter(*args,**kwargs)

            self.ignoreEvents = False

        