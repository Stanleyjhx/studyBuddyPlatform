import mysql.connector
from flask_restful import Resource, Api, fields, marshal_with
from backend.database.dao.mysql_dao_model import DAO
from backend.endpoint import utils
from backend.endpoint.register import vars
from flask import Blueprint, current_app, request
from backend.database.dao.redis_dao_model import *

app_register = Blueprint(name="app_register", import_name="backend.endpoint.route")
api_register = Api(app_register)

response = {
    'status': fields.Integer,
    'data': fields.Raw,
    'error': fields.String,
}


class CreateUser(Resource):
    @marshal_with(response)
    def post(self, ):
        args = utils.get_parser(vars.CreateUserReqeust, "post").parse_args()

        user_name = args.get("user_name")
        password = args.get("password")
        email = args.get("email")
        first_name = args.get("first_name")
        last_name = args.get("last_name")
        student_id = args.get("student_id")
        major = args.get("major") if args.get("major") is not None else ""
        description = args.get("description") if args.get("description") is not None else ""

        if not utils.check_email_format(email):
            return utils.invalid_email_format_response()
        request.cnx.start_transaction()
        cursor = request.cnx.cursor(dictionary=True)
        dao_object = DAO(utils.table_names["users"], logger=current_app.logger, cursor=cursor)

        try:
            cursor.execute(dao_object.Insert(value={
                "user_name": user_name,
                "password": password,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "student_id": student_id,
                "major": major,
                "description": description,
                "is_deleted": 0,
            }))
            cursor.execute(dao_object.GetLastRow(
                column="user_id"
            ))
            user_id = cursor.fetchone()['user_id']
            vars.SendEmail(email=email, user_id=user_id)
            request.cnx.commit()
            cursor.close()
            return vars.CreateUserResponse()

        except mysql.connector.Error as err:
            request.cnx.rollback()
            cursor.close()
            return utils.err_response(err)


class VerifyEmail(Resource):
    @marshal_with(response)
    def post(self):
        args = utils.get_parser(vars.VerifyEmailRequest, "post").parse_args()
        email = args.get("email")
        code_client = args.get("verification_code")

        # Check in redis
        code_host = tredis.get(email)
        if code_host is not None:
            code_host = str(int(code_host))
            return vars.EmailVerifiedResponse() if code_host == code_client else vars.InvalidCodeResponse()
        else:
            return vars.CodeExpirationResponse()


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
                               logger=current_app.logger,
                               cursor=cursor)
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


@app_register.before_request
def before_request():
    cnx = mysql.connector.connect(user='root',
                                  password='qwertyui',
                                  host='127.0.0.1',
                                  database='StudyBuddy')
    setattr(request, "cnx", cnx)


@app_register.after_request
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
    # resp.headers['Access-Control-Allow-Origin'] = utils.react_ip
    resp.headers['Access-Control-Allow-Credentials'] = "true"
    resp.headers['Access-Control-Allow-Method'] = "GET,POST,PUT,DELETE"
    resp.headers['Access-Control-Allow-Headers'] = "Content-Type,Authorization,Origin"
    return resp


# Group Detail Apis
api_register.add_resource(CreateUser, '/create_user')
api_register.add_resource(VerifyEmail, '/verify_email')
api_register.add_resource(Verify, '/verify/<string:token>')

