from flask import jsonify, Blueprint
from datetime import datetime


blueprint = Blueprint(name='healthcheck', import_name=__name__)


@blueprint.get('/healthcheck')
def healthcheck():
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    health_status = {'status': 'OK', 'date': current_date}
    return jsonify(health_status)
