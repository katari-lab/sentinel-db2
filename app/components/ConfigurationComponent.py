import os


class ConfigurationComponent:
    def __init__(self):

        self.database = os.environ.get('DATABASE') or "sutdb"
        self.host = os.environ.get('host') or "localhost"
        self.port = os.environ.get('port') or "50000"
        self.username = os.environ.get('username') or "db2inst1"
        self.password = os.environ.get('password') or "admin123"

    def get_connection(self):
        cs = "DATABASE={};HOSTNAME={};PORT={};PROTOCOL=TCPIP;UID={};PWD={};".format(self.database,
                                                                                    self.host,
                                                                                    self.port,
                                                                                    self.username,
                                                                                    self.password)
        return cs
