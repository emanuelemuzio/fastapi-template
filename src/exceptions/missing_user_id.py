class MissingUserIdException(Exception):
    """Exception raised for custom error scenarios.
    """

    def __init__(self, idx):
        self.message = f"User with id: {idx} does not exist"
        super().__init__(self.message)