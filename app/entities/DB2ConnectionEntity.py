class DB2ConnectionEntity:
    def __init__(self, state: dict):
        self.database = state.get('DATABASE', "sutdb")
        self.host = state.get('host', "localhost")
        self.port = state.get('port', "50000")
        self.username = state.get('username', "db2inst1")
        self.password = state.get('password', "admin123")

    def get_connection(self):
        cs = "DATABASE={};HOSTNAME={};PORT={};PROTOCOL=TCPIP;UID={};PWD={};".format(self.database,
                                                                                    self.host,
                                                                                    self.port,
                                                                                    self.username,
                                                                                    self.password)
        return cs