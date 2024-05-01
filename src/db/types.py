class BaseType:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        if self.has_default_value():
            return str(self.kwargs.get('default'))
        
    def has_default_value(self):
        return 'default' in self.kwargs

class Integer(BaseType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Float(BaseType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class String(BaseType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Text(BaseType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Boolean(BaseType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Datetime(BaseType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)