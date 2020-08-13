from flask import Blueprint, render_template, abort, request, jsonify

from app.components.ConnectionsComponent import ConnectionsComponent
from app.components.DB2Component import DB2Component
from app.entities.DB2ConnectionEntity import DB2ConnectionEntity

import os
from app.entities.DB2QueryEntity import DB2QueryEntity


log_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.abspath(os.path.join(log_dir, os.pardir))
log_dir = os.path.abspath(os.path.join(log_dir, os.pardir))
log_dir = os.path.abspath(os.path.join(log_dir, "logs"))


thread_pool = dict()
blueprint = Blueprint('db2_blueprint', __name__)
db2_connections = DB2Component()
db2_connection_summary = ConnectionsComponent(log_dir)


@blueprint.route('/summary/connections', methods=['POST', 'DELETE'])
def connect():
    if request.method == "POST":
        payload = request.get_json() or {}
        entity = DB2QueryEntity(payload)
        db2_connections.validate_connection(entity)
        db2_connection_summary.enable_connection_summary_task(entity)
    elif request.method == "DELETE":
        db2_connection_summary.disable_connection_summary_task()
    response = {"connection_summary": db2_connection_summary.enable_connection_summary}
    return jsonify(response)








