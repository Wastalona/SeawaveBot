class ProfessionException(Exception):
    def __init__(self, message="This profession is not registered or has not been found."):
        super().__init__(message)

class StaffEditException(Exception):
    def __init__(self, message):
        super().__init__(message)

class IdValueException(Exception):
    def __init__(self, message, input_value):
        super().__init__(message)
        self.input_value = input_value

class NotifyException(Exception):
    def __init__(self, message):
        super().__init__(message)