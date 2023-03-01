from flask import Flask
from flask_restful import Resource, Api, fields, marshal_with
from backend.dao.dao_model import DAO
from backend.endpoint import utils
from backend.endpoint.group import vars

app_group = Flask(__name__)
api = Api(app_group)

response = {
    'status': fields.Integer,
    'data': fields.Raw,
    'error': fields.String,
}


class GetTotalGroupsCount(Resource):
    @marshal_with(response)
    # fetch groups in a paginated manner
    def get(self):
        groups_dao_object = DAO(utils.table_names["groups"], logger=app_group.logger)
        total_groups_count, err = groups_dao_object.Count(filter_by="is_deleted = 0")

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


class GetGroups(Resource):
    @marshal_with(response)
    # fetch groups in a paginated manner
    def get(self):
        args = utils.get_parser(vars.GetGroupReqeust).parse_args()

        order_by = args.get("order_by")
        limit = args.get("limit")
        offset = args.get("offset")
        show_deleted = args.get("show_deleted")

        groups_dao_object = DAO(utils.table_names["groups"], logger=app_group.logger)
        number_of_groups, groups, err = groups_dao_object.GetWithPagination(column="group_id, group_name, group_owner, group_description",
                                                                            filter_by="is_deleted = 0" if show_deleted is False else "1",
                                                                            limit=limit,
                                                                            offset=offset,
                                                                            order_by=order_by if order_by is not None else "1")

        del groups_dao_object

        if err is not None:
            return {
                "status": 400,
                "error": "Mysql facing error : {}".format(str(err)),
            }
        return {
            "status": 200,
            "data": {
                "number_of_groups": number_of_groups,
                "groups": list(groups)
            },
        }


class CreateGroup(Resource):
    @marshal_with(response)
    def post(self):
        # fetch groups in a paginated manner
        args = utils.get_parser(vars.CreateGroupReqeust).parse_args()

        group_name = args.get("group_name")

        groups_dao_object = DAO(utils.table_names["groups"], logger=app_group.logger)
        err = groups_dao_object.Insert(value={
            "group_name": "'{}'".format(group_name),
            "is_deleted": "false",
        })

        del groups_dao_object

        if err is not None:
            return {
                "status": 400,
                "error": "Mysql facing error : {}".format(str(err)),
            }
        return {
            "status": 200,
        }


class EditGroup(Resource):
    def post(self, group_id):
        # fetch groups in a paginated manner
        args = utils.get_parser(vars.EditGroupReqeust).parse_args()

        edit_contents = args.get("edit_contents")

        groups_dao_object = DAO(utils.table_names["groups"], logger=app_group.logger)

        if args.get("edit_type") == utils.EditType.Delete:
            err = groups_dao_object.Update(value={"is_deleted": "true"},
                                           filter_by="group_id={}".format(group_id))

        elif args.get("edit_type") == utils.EditType.Edit:
            app_group.logger.info(args.get("edit_contents"))
            err = groups_dao_object.Update(value=edit_contents,
                                           filter_by="group_id = {}".format(group_id))

        del groups_dao_object

        if err is not None:
            return {
                "status": 400,
                "error": "Mysql facing error : {}".format(str(err)),
            }
        return {
            "status": 200,
        }

