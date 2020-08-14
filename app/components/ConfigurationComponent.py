import os


class ConfigurationComponent:

    @staticmethod
    def get_interval():
        return os.environ.get('interval') or 10

    @staticmethod
    def get_log_dir():
        log_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.abspath(os.path.join(log_dir, os.pardir))
        log_dir = os.path.abspath(os.path.join(log_dir, os.pardir))
        return os.path.abspath(os.path.join(log_dir, "logs"))

    @staticmethod
    def get_trace_name():
        prefix = os.environ.get('prefix') or os.environ.get('database') or "sutdb"
        return prefix

    @staticmethod
    def get_connection():
        database = os.environ.get('database') or "sutdb"
        host = os.environ.get('host') or "localhost"
        port = os.environ.get('port') or "50000"
        username = os.environ.get('username') or "db2inst1"
        password = os.environ.get('password') or "admin123"
        cs = "DATABASE={};HOSTNAME={};PORT={};PROTOCOL=TCPIP;UID={};PWD={};".format(database,
                                                                                    host,
                                                                                    port,
                                                                                    username,
                                                                                    password)
        return cs
