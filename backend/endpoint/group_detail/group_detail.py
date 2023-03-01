from flask import Flask, request
from flask_restful import Resource, Api, fields, marshal_with
from backend.dao.dao_model import DAO
from backend.endpoint import utils
from backend.endpoint.group_detail import vars

app_group_detail = Flask(__name__)
api = Api(app_group_detail)

response = {
    'status': fields.Integer,
    'data': fields.Raw,
    'error': fields.String,
}


class GetStudyPlanByGroup(Resource):
    @marshal_with(response)
    # fetch groups in a paginated manner
    def get(self, group_id):
        args = utils.get_parser(vars.GetStudyPlanReqeust).parse_args()

        limit = args.get("limit")
        offset = args.get("offset")
        order_by = args.get("order_by")

        groups_dao_object = DAO(utils.table_names["study_plan"], logger=app_group_detail.logger)

        count, study_plans, err = groups_dao_object.GetWithPagination(
            column="event_id, group_id, event_holder, event_name, "
                   "event_description, DATE_FORMAT(start_time, '%Y-%m-%d %T.%f') "
                   "as start_time",
            filter_by="group_id={}".format(group_id),
            order_by=order_by if order_by is not None else "1",
            limit=limit,
            offset=offset,
        )

        del groups_dao_object

        if err is not None:
            return {
                "status": 400,
                "error": "Mysql facing error : {}".format(str(err)),
            }
        return {
            "status": 200,
            "data": {
                "number_of_study_plan": count,
                "study_plan": list(study_plans),
            },
        }


class GetStudyPlan(Resource):
    @marshal_with(response)
    # fetch groups in a paginated manner
    def get(self, study_plan_id):
        args = utils.get_parser(vars.GetStudyPlanReqeust).parse_args()

        groups_dao_object = DAO(utils.table_names["study_plan"], logger=app_group_detail.logger)

        study_plans, err = groups_dao_object.Get(
            column="event_id, group_id, event_holder, event_name, "
                   "event_description, DATE_FORMAT(start_time, '%Y-%m-%d %T.%f') "
                   "as start_time",
            filter_by="event_id={}".format(study_plan_id)
        )

        del groups_dao_object

        if err is not None:
            return {
                "status": 400,
                "error": "Mysql facing error : {}".format(str(err)),
            }
        elif len(study_plans) == 0:
            return {
                "status": 200,
                "error": "Study Plan {} doesn't exist".format(study_plan_id),
            }
        else:
            return {
                "status": 200,
                "data": {
                    "number_of_study_plan": len(study_plans),
                    "study_plan": study_plans[0],
                },
            }


