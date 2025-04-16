class ExistingUserEmail(Exception):
    """Exception raised for custom error scenarios.
    """

    def __init__(self, email):
        self.message = f"User with email: {email} already exists"
        super().__init__(self.message)