class JsonNotFoundException(Exception):
    """Exception raised for custom error scenarios.

    Attributes:
        filename -- name of the JSON file missing
    """

    def __init__(self, filename):
        self.message = f"JSON file not found: {filename}"
        super().__init__(self.message)