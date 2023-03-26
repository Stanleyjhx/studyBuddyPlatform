import mysql.connector
from flask_restful import Resource, Api, fields, marshal_with
from backend.database.dao.mysql_dao_model import DAO
from backend.endpoint import utils
from backend.endpoint.SES import vars
from backend.database.dao.redis_dao_model import tredis
from flask import Blueprint, current_app, request

app_notification = Blueprint(name="app_notification", import_name="backend.endpoint.route")
api_notification = Api(app_notification)

response = {
    'status': fields.Integer,
    'data': fields.Raw,
    'error': fields.String,
}


class Verify(Resource):
    @marshal_with(response)
    # fetch groups in a paginated manner
    def get(self, token):
        user_id = tredis.get(token)
        if user_id == "":
            return utils.err_response('Verification Status Expired')
        else:
            user_id = int(user_id)
        cursor = request.cnx.cursor(dictionary=True, buffered=True)
        users_dao_object = DAO(table_name=utils.table_names["users"],
                               logger=current_app.logger)
        try:
            request.cnx.start_transaction()
            cursor.execute(users_dao_object.Update(
                value={"status": 1},
                filter_by="user_id = {}".format(user_id),
            ))
            request.cnx.commit()
            cursor.close()
            return vars.VerifyResponse()

        except mysql.connector.Error as err:
            request.cnx.rollback()
            cursor.close()
            request.cnx.close()
            return utils.err_response("MySQL facing error : {}".format(err))


@app_notification.before_request
def before_request():
    cnx = mysql.connector.connect(user='sbp',
                                  password='sbp',
                                  host='127.0.0.1',
                                  database='sbp',
                                  pool_size=32)
    cnx.autocommit = False
    setattr(request, "cnx", cnx)


@app_notification.after_request
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = utils.react_ip
    resp.headers['Access-Control-Allow-Credentials'] = "true"
    resp.headers['Access-Control-Allow-Method'] = "GET,POST,PUT,DELETE"
    resp.headers['Access-Control-Allow-Headers'] = "Content-Type,Authorization,Origin"
    return resp


# Group Detail Apis
api_notification.add_resource(Verify, '/verify/<string:token>')
