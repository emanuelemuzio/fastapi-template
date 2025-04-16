class InvalidJsonFormatException(Exception):
    """Exception raised for custom error scenarios.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, filename):
        self.message = f"JSON file not found: {filename}"
        super().__init__(self.message)