class Connection:

    def __init__(self, username: str, password: str, host: str, port: int, database: str) -> None:
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database