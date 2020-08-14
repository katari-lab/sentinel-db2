# https://github.com/prometheus/client_python
from flask import Flask
from app.agents.ConnectionsAgent import ConnectionsAgent
from app.components.ConfigurationComponent import ConfigurationComponent
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
import logging
import sys


logging.basicConfig(filename='./../logs/app.log', level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})


@app.route('/')
def hello_world():
    return 'db2 sentinel!'


if __name__ == '__main__':
    logging.info('start db2 sentinel')
    logging.info('connection {}'.format(ConfigurationComponent.get_connection()))
    ConnectionsAgent.connection_summary()
    app.run(host='0.0.0.0', debug=True)
