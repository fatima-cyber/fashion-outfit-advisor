class SessionManager:
    """
    Manages session IDs for chat interactions.

    This class provides methods to create, retrieve, and manipulate session IDs.
    It maintains a single counter for generating unique session IDs.

    Attributes:
        current_id (int): The current session ID counter.

    Methods:
        get_new_session_id(): Increments and returns a new session ID.
        clear_session_id(): Resets the session ID counter to 0.
        get_session_id(): Returns the current session ID.
        set_session_id(id): Sets the session ID to a specific value.
    """

    def __init__(self):
        self.current_id = 0

    def get_new_session_id(self):
        self.current_id += 1
        return self.current_id

    def clear_session_id(self):
        self.current_id = 0

    def get_session_id(self):
        return self.current_id

    def set_session_id(self, id):
        self.current_id = id