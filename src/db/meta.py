class MetaField:
    def __init__(self, model, fields):
        self.fields = fields
        self.model = model
    
    @property
    def values(self):
        vals = [getattr(self.model, field) for field in self.fields]
        return vals