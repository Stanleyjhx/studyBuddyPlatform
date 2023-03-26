import mysql.connector
import uuid
from flask_restful import Resource, Api, fields, marshal_with
from backend.database.dao.mysql_dao_model import DAO
from backend.endpoint.login import vars
from flask import Blueprint, current_app, request
from backend.database.dao.redis_dao_model import *


app_login = Blueprint(name="app_login", import_name="backend.endpoint.route")
api_login = Api(app_login)

response = {
    'status': fields.Integer,
    'data': fields.Raw,
    'error': fields.String,
}


class Authenticate(Resource):
    @marshal_with(response)
    def post(self, ):
        args = utils.get_parser(vars.Authentication_req, "post").parse_args()

        identifier = args.get("identifier")
        password = args.get("password")
        request.cnx.start_transaction()
        cursor = request.cnx.cursor(dictionary=True)
        auth_dao_object = DAO(utils.table_names["users"], logger=current_app.logger, cursor=cursor)

        try:
            # Fetch password from DB
            if utils.check_email_format(identifier):
                cursor.execute(auth_dao_object.Get(
                    column="user_id, password, email, status",
                    filter_by="is_deleted = 0 and email = '{}'".format(identifier)))
            else:
                cursor.execute(auth_dao_object.Get(
                    column="user_id, password, user_name, status",
                    filter_by="is_deleted = 0 and user_name = '{}'".format(identifier)))
            if cursor.rowcount == 0:
                return vars.unauthenticated_response()

            # Match password
            result = cursor.fetchone()
            if result is None:
                return vars.unauthenticated_response()
            request.cnx.commit()
            cursor.close()
            if (result['password'] == password) & (result['status'] == 1):
                access_token = str(uuid.uuid4())
                tredis.set(name=utils.get_session_key(access_token), value=result['user_id'], ex=18000)
                return vars.authenticated_response(access_token)
            else:
                return vars.unauthenticated_response()

        except mysql.connector.Error as err:
            request.cnx.rollback()
            cursor.close()
            return utils.err_response(err)


@app_login.before_request
def before_request():
    cnx = mysql.connector.connect(user='root',
                                  password='qwertyui',
                                  host='127.0.0.1',
                                  database='StudyBuddy')
    setattr(request, "cnx", cnx)


@app_login.after_request
def after_request(resp):
    # resp.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
    resp.headers['Access-Control-Allow-Credentials'] = "true"
    resp.headers['Access-Control-Allow-Method'] = "GET,POST,PUT,DELETE"
    resp.headers['Access-Control-Allow-Headers'] = "Content-Type,Authorization,Origin"
    return resp


# Login Apis
api_login.add_resource(Authenticate, '/auth')

