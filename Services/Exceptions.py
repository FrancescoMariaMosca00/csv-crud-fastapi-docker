class ValidationError(Exception):
    pass

class DuplicateIDError(ValidationError):
    pass

class InvalidCodeFiscaleError(ValidationError):
    pass

class InvalidNameError(ValidationError):
    pass

class ItemNotFound(Exception):
    pass