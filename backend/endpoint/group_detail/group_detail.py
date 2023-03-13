import mysql.connector
from flask_restful import Resource, Api, fields, marshal_with
from backend.database.dao.mysql_dao_model import DAO
from backend.endpoint import utils
from backend.endpoint.group_detail import vars
from backend.database.dao.mysql_dao_model import cnx
from flask import Blueprint, current_app, request
from backend.database.dao.redis_dao_model import *

app_group_detail = Blueprint(name="app_group_detail", import_name="backend.endpoint.route")
api_group_detail = Api(app_group_detail)

response = {
    'status': fields.Integer,
    'data': fields.Raw,
    'error': fields.String,
}


class GetStudyPlanByGroup(Resource):
    @marshal_with(response)
    # fetch groups in a paginated manner
    def get(self, group_id):
        args = utils.get_parser(vars.GetStudyPlanByGroupReqeust).parse_args()

        limit = args.get("limit")
        offset = args.get("offset")
        order_by = args.get("order_by")

        try:
            cursor = cnx.cursor(dictionary=True, buffered=True)
            dao_object = DAO(utils.table_names["study_plan"], logger=current_app.logger, cursor=cursor)
            cursor.execute(dao_object.GetWithPagination(
                column="event_id, group_id, event_holder, event_name, "
                       "event_description, DATE_FORMAT(start_time, '%Y-%m-%d %T') "
                       "as start_time , DATE_FORMAT("
                       "end_time, '%Y-%m-%d %T') as end_time",
                filter_by="group_id={}".format(group_id),
                order_by=order_by if order_by is not None else "1",
                limit=limit,
                offset=offset,
            ))
            result = vars.GetStudyPlanByGroupResponse(cursor.rowcount, cursor.fetchall())
            cursor.close()
            return result
        except mysql.connector.Error as err:
            cursor.close()
            return utils.err_response("MySQL facing error : {}".format(err))


class GetStudyPlanById(Resource):
    @marshal_with(response)
    # fetch groups in a paginated manner
    def get(self, study_plan_id):
        cursor = cnx.cursor(dictionary=True, buffered=True)
        groups_dao_object = DAO(utils.table_names["study_plan"], logger=current_app.logger, cursor=cursor)
        try:
            cursor.execute(groups_dao_object.Get(
                column="event_id, group_id, event_holder, event_name, "
                       "event_description, DATE_FORMAT(start_time, '%Y-%m-%d %T') as start_time, DATE_FORMAT("
                       "end_time, '%Y-%m-%d %T') as end_time",
                filter_by="event_id={}".format(study_plan_id)
            ))
            if cursor.rowcount == 0:
                return utils.err_response("Study Plan {} doesn't exist".format(study_plan_id))
            else:
                return vars.GetStudyPlanResponse(cursor.fetchone())

        except mysql.connector.Error as err:
            cursor.close()
            return utils.err_response("MySQL facing error : {}".format(err))


class CreateStudyPlan(Resource):
    @marshal_with(response)
    # fetch groups in a paginated manner
    def post(self, group_id):
        args = utils.get_parser(vars.CreateStudyPlanReqeust, "post").parse_args()

        capacity = args.get("capacity")
        event_name = args.get("event_name")
        start_time = args.get("start_time")
        end_time = args.get("end_time")
        location = args.get("location") if args.get("location") is not None else ""
        event_description = args.get("description") if args.get("description") is not None else ""
        user_id = int(request.user_id)

        cnx.start_transaction()
        cursor = cnx.cursor(dictionary=True)
        dao_object = DAO(utils.table_names["study_plan"], logger=current_app.logger, cursor=cursor)

        try:
            cursor.execute(dao_object.Insert(value={
                "event_name": event_name,
                "capacity": capacity,
                "start_time": start_time,
                "end_time": end_time,
                "location": location,
                "event_description": event_description,
                "group_id": group_id,
                "event_holder": user_id,
                "is_deleted": 0,
            }))
            cnx.commit()
            cursor.close()
            return vars.CreateStudyPlanResponse()

        except mysql.connector.Error as err:
            cnx.rollback()
            cursor.close()
            return utils.err_response(err)


class EditStudyPlan(Resource):
    @marshal_with(response)
    # fetch groups in a paginated manner
    def post(self, study_plan_id):
        args = utils.get_parser(vars.EditStudyPlanReqeust, "post").parse_args()

        edit_type = args.get("edit_type")
        edit_contents = args.get("edit_contents")
        user_id = int(request.user_id)

        cnx.start_transaction()
        cursor = cnx.cursor(dictionary=True, buffered=True)
        dao_object = DAO(utils.table_names["study_plan"], logger=current_app.logger, cursor=cursor)

        try:
            cursor.execute(dao_object.Get(column="event_holder", filter_by="event_id = {}".format(study_plan_id)))
            if cursor.fetchone()["event_holder"] != user_id:
                cnx.rollback()
                cursor.close()
                return utils.lack_permission_response(user_id)
            if edit_type == utils.EditType.Delete:
                cursor.execute(dao_object.Update(value={"is_deleted": "true"},
                                                 filter_by="event_id = {}".format(study_plan_id)))
            elif edit_type == utils.EditType.Edit:
                current_app.logger.info(args.get("edit_contents"))
                cursor.execute(dao_object.Update(value=edit_contents,
                                                 filter_by="event_id = {}".format(study_plan_id)))

            cnx.commit()
            cursor.close()
            return vars.CreateStudyPlanResponse()

        except mysql.connector.Error as err:
            cnx.rollback()
            cursor.close()
            return utils.err_response(err)


@app_group_detail.before_request
def before_request():
    token = request.headers.get("Authorization")
    if not token:
        return utils.unauthenticated_response()

    user_id = utils.validate_session(token.split()[1])
    if user_id is None:
        return utils.unauthenticated_response()
    else:
        setattr(request, "user_id", user_id)

@app_group_detail.after_request
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = utils.react_ip
    resp.headers['Access-Control-Allow-Credentials'] = "true"
    resp.headers['Access-Control-Allow-Method'] = "GET,POST,PUT,DELETE"
    resp.headers['Access-Control-Allow-Headers'] = "Content-Type,Authorization,Origin"
    return resp


# Group Detail Apis
api_group_detail.add_resource(GetStudyPlanByGroup, '/get_study_plan_by_group/<int:group_id>')
api_group_detail.add_resource(GetStudyPlanById, '/get_study_plan_by_id/<int:study_plan_id>')
api_group_detail.add_resource(CreateStudyPlan, '/create_study_plan/<int:group_id>')
api_group_detail.add_resource(EditStudyPlan, '/edit_study_plan/<int:study_plan_id>')

