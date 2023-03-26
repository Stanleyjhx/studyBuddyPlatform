import mysql.connector
from flask_restful import Resource, Api, fields, marshal_with
from backend.database.dao.mysql_dao_model import DAO
from backend.endpoint import utils
from backend.endpoint.personal_info import vars
from flask import Blueprint, current_app, request, session
from backend.database.dao.redis_dao_model import *

app_personal_info = Blueprint(name="app_personal_info", import_name="backend.endpoint.route")
api_personal_info = Api(app_personal_info)

response = {
    'status': fields.Integer,
    'data': fields.Raw,
    'error': fields.String,
}


class GetPersonalInfo(Resource):
    @marshal_with(response)
    # fetch user information
    def get(self):
        user_id = int(request.user_id)
        cursor = request.cnx.cursor(dictionary=True, buffered=True)
        users_dao_object = DAO(table_name=utils.table_names["users"], logger=current_app.logger, cursor=cursor)
        try:
            cursor.execute(users_dao_object.Get(
                column="user_name, first_name, last_name, student_id, email, major, description, "
                       "DATE_FORMAT(created_at, '%Y-%m-%d %T') as created_at",
                filter_by="is_deleted = 0 and user_id = {}".format(user_id)))
            if cursor.rowcount == 0:
                return utils.err_response("User_id {} doesn't exist".format(user_id))
            else:
                result = vars.GetPersonalInfoResponse(cursor.fetchone())
                cursor.close()
                return result

        except mysql.connector.Error as err:
            cursor.close()
            return utils.err_response("MySQL facing error : {}".format(err))


class EditPersonalInfo(Resource):
    def post(self):
        user_id = int(request.user_id)
        args = utils.get_parser(vars.EditPersonalInfoReqeust, "post").parse_args()

        edit_contents = args.get("edit_contents")
        edit_type = args.get("edit_type")

        cursor = request.cnx.cursor(dictionary=True)
        users_dao_object = DAO(utils.table_names["users"], logger=current_app.logger, cursor=cursor)

        try:
            if edit_type == utils.EditType.Delete:
                cursor.execute(users_dao_object.Update(value={"is_deleted": 1},
                                                       filter_by="user_id = {}".format(user_id)))

            elif edit_type == utils.EditType.Edit:
                current_app.logger.info(args.get("edit_contents"))
                cursor.execute(users_dao_object.Update(value=edit_contents,
                                                       filter_by="user_id = {}".format(user_id)))

            request.cnx.commit()
            cursor.close()
            return vars.EditPersonalInfoResponse()

        except mysql.connector.Error as err:
            request.cnx.rollback()
            cursor.close()
            return utils.err_response("MySQL facing error : {}".format(err))


@app_personal_info.before_request
def before_request():
    current_app.logger.info(request.headers)
    token = request.headers.get("Authorization")
    cnx = mysql.connector.connect(user='root',
                                  password='qwertyui',
                                  host='127.0.0.1',
                                  database='StudyBuddy')
    if not token:
        return utils.unauthenticated_response()
    user_id = utils.validate_session(token.split()[1])
    if user_id is None:
        return utils.unauthenticated_response()
    else:
        setattr(request, "user_id", user_id)
        setattr(request, "cnx", cnx)


@app_personal_info.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
    response.headers['Access-Control-Allow-Credentials'] = "true"
    response.headers['Access-Control-Allow-Method'] = "GET,POST,PUT,DELETE"
    response.headers['Access-Control-Allow-Headers'] = "Origin,Authorization,content-type"
    return response


# Personal-info Apis
api_personal_info.add_resource(GetPersonalInfo, '/get_personal_info')
api_personal_info.add_resource(EditPersonalInfo, '/edit_personal_info')
