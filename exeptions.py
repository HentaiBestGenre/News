class TooManyRequests(Exception):
    def __init__(self) -> None:
        super().__init__("Too Many Requests")