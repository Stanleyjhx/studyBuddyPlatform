import mysql.connector
from flask_restful import Resource, Api, fields, marshal_with
from backend.dao.dao_model import DAO
from backend.endpoint import utils
from backend.endpoint.group_detail import vars
from backend.dao.dao_model import cnx
from flask import Blueprint, current_app

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
            groups_dao_object = DAO(utils.table_names["study_plan"], logger=current_app.logger, cursor=cursor)
            cursor.execute(groups_dao_object.GetWithPagination(
                column="event_id, group_id, event_holder, event_name, "
                       "event_description, DATE_FORMAT(start_time, '%Y-%m-%d %T.%f') "
                       "as start_time",
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


class GetStudyPlan(Resource):
    @marshal_with(response)
    # fetch groups in a paginated manner
    def get(self, study_plan_id):
        cursor = cnx.cursor(dictionary=True, buffered=True)
        groups_dao_object = DAO(utils.table_names["study_plan"], logger=current_app.logger, cursor=cursor)
        try:
            cursor.execute(groups_dao_object.Get(
                column="event_id, group_id, event_holder, event_name, "
                       "event_description, DATE_FORMAT(start_time, '%Y-%m-%d %T.%f') as start_time, DATE_FORMAT("
                       "end_time, '%Y-%m-%d %T.%f') as end_time",
                filter_by="event_id={}".format(study_plan_id)
            ))
            if cursor.rowcount == 0:
                return utils.err_response("Study Plan {} doesn't exist".format(study_plan_id))
            else:
                return vars.GetStudyPlanResponse(cursor.fetchone())

        except mysql.connector.Error as err:
            cursor.close()
            return utils.err_response("MySQL facing error : {}".format(err))


# Group Detail Apis
api_group_detail.add_resource(GetStudyPlanByGroup, '/get_study_plan_by_group/<int:group_id>')
api_group_detail.add_resource(GetStudyPlan, '/get_study_plan_by_id/<int:study_plan_id>')
