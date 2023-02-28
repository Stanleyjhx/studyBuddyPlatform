from flask import Flask, request
from flask_restful import Resource, Api, fields, marshal_with
from backend.dao.dao_model import DAO
from backend.endpoint import utils
import vars

app_group_detail = Flask(__name__)
api = Api(app_group_detail)

response = {
    'status': fields.Integer,
    'data': fields.Raw,
    'error': fields.String,
}


class GetGroupStudyPlan(Resource):
    @marshal_with(response)
    # fetch groups in a paginated manner
    def get(self):
        args = utils.get_parser(vars.GetStudyPlanReqeust).parse_args()
        app_group_detail.logger.info(args)
        groups_dao_object = DAO(vars.table_names["study_plan"], logger=app_group_detail.logger)

        if args.get("filter_type") == vars.FilterType.FilterByGroupID:

            return {
                "status": 200,
                "error": "invalid parameter, fail fetching group_id",
            }

        total_groups_count, err = groups_dao_object.Count(filter_by="group_id = 0")

        del groups_dao_object

        if err is not None:
            return {
                "status": 400,
                "error": "Mysql facing error : {}".format(str(err)),
            }
        return {
            "status": 200,
            "data": {
                "number_of_groups": total_groups_count,
            },
        }


api.add_resource(GetGroupStudyPlan, '/get_group_study_plan')


if __name__ == '__main__':
    app_group_detail.run(debug=True)
