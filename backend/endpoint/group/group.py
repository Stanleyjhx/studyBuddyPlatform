import os

import mysql.connector
from flask_restful import Resource, Api, fields, marshal_with
from backend.database.dao.mysql_dao_model import DAO
from backend.endpoint import utils
from backend.endpoint.group import vars
from backend.database.dao.mysql_dao_model import cnx
from flask import Blueprint, current_app, request, session
from backend.database.dao.redis_dao_model import *

app_group = Blueprint(name="app_group", import_name="backend.endpoint.route")
api_group = Api(app_group)

response = {
    'status': fields.Integer,
    'data': fields.Raw,
    'error': fields.String,
}


class GetTotalGroupsCount(Resource):
    @marshal_with(response)
    # fetch groups in a paginated manner
    def get(self):
        total_groups_count = tredis.get(utils.get_groups_count_key())
        if total_groups_count is not None:
            return {
                "status": 200,
                "data": {
                    "number_of_groups": int(total_groups_count)
                },
            }
        else:
            cursor = cnx.cursor(buffered=True)
            groups_dao_object = DAO(table_name=utils.table_names["groups"], logger=current_app.logger, cursor=cursor)
            try:
                cursor.execute(groups_dao_object.Count(filter_by="is_deleted = 0"))
                cnx.commit()
                total_groups_count = cursor.fetchone()[0]
                cursor.close()
                tredis.set(utils.get_groups_count_key(), total_groups_count)
                return {
                    "status": 200,
                    "data": {
                        "number_of_groups": total_groups_count,
                    },
                }
            except mysql.connector.Error as err:
                cnx.rollback()
                return utils.err_response(err)


class GetGroups(Resource):
    @marshal_with(response)
    # fetch groups in a paginated manner
    def get(self):
        args = utils.get_parser(vars.GetGroupReqeust).parse_args()

        order_by = args.get("order_by")
        limit = args.get("limit")
        offset = args.get("offset")

        cursor = cnx.cursor(dictionary=True, buffered=True)
        groups_dao_object = DAO(utils.table_names["groups"], logger=current_app.logger, cursor=cursor)

        try:
            cursor.execute(groups_dao_object.GetWithPagination(column="group_id, group_name, group_owner, "
                                                                      "group_description",
                                                               filter_by="is_deleted = 0",
                                                               limit=limit,
                                                               offset=offset,
                                                               order_by=order_by if order_by is not None else "1"))
            cnx.commit()
            result = vars.GetGroupsResponse(cursor.rowcount, list(cursor.fetchall()))
            cursor.close()
            return result

        except mysql.connector.Error as err:
            cnx.rollback()
            cursor.close()
            return utils.err_response(err)


class CreateGroup(Resource):
    @marshal_with(response)
    def post(self):
        # fetch groups in a paginated manner
        args = utils.get_parser(vars.CreateGroupReqeust, "post").parse_args()

        group_name = args.get("group_name")
        token = request.headers.get("Authorization")
        user_id = utils.validate_session(token.split()[1])
        group_owner = args.get("group_owner")
        group_description = args.get("group_description").replace("'", "\'")

        cnx.start_transaction()
        cursor = cnx.cursor(dictionary=True)
        groups_dao_object = DAO(utils.table_names["groups"], logger=current_app.logger, cursor=cursor)
        group_member_dao_object = DAO(utils.table_names["group_members"], logger=current_app.logger, cursor=cursor)

        try:
            cursor.execute(groups_dao_object.Insert(value={
                "group_name": group_name,
                "group_owner": user_id,
                "group_description": group_description,
                "is_deleted": 0,
            }))
            last_row_id = cursor.lastrowid
            cursor.execute(group_member_dao_object.Insert(value={
                "group_id": last_row_id,
                "user_id": group_owner,
            }))
            cnx.commit()
            result = vars.CreateGroupResponse(last_row_id)
            cursor.close()

            return result

        except mysql.connector.Error as err:
            cnx.rollback()
            cursor.close()
            return utils.err_response(err)


class EditGroup(Resource):
    def post(self, group_id):
        # fetch groups in a paginated manner
        args = utils.get_parser(vars.EditGroupReqeust, "post").parse_args()

        edit_contents = args.get("edit_contents")
        edit_type = args.get("edit_type")

        cursor = cnx.cursor(dictionary=True)
        groups_dao_object = DAO(utils.table_names["groups"], logger=current_app.logger, cursor=cursor)

        try:
            if edit_type == utils.EditType.Delete:
                cursor.execute(groups_dao_object.Update(value={"is_deleted": "true"},
                                                        filter_by="group_id = {}".format(group_id)))

            elif edit_type == utils.EditType.Edit:
                current_app.logger.info(args.get("edit_contents"))
                cursor.execute(groups_dao_object.Update(value=edit_contents,
                                                        filter_by="group_id = {}".format(group_id)))

            cnx.commit()
            cursor.close()
            return vars.EditGroupResponse()

        except mysql.connector.Error as err:
            cnx.rollback()
            cursor.close()
            return utils.err_response("MySQL facing error : {}".format(err))


@app_group.before_request
def before_request():
    token = request.headers.get("Authorization")
    if not token:
        return utils.unauthenticated_response()

    user_id = utils.validate_session(token.split()[1])
    if user_id is None:
        return utils.unauthenticated_response()
    else:
        setattr(request, "user_id", user_id)


@app_group.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = utils.react_ip
    response.headers['Access-Control-Allow-Credentials'] = "true"
    response.headers['Access-Control-Allow-Method'] = "GET,POST,PUT,DELETE"
    response.headers['Access-Control-Allow-Headers'] = "Origin,Authorization"
    return response


# Group Apis
api_group.add_resource(GetTotalGroupsCount, '/get_total_groups_count')
api_group.add_resource(GetGroups, '/get_groups')
api_group.add_resource(CreateGroup, '/create_group')
api_group.add_resource(EditGroup, '/edit_group/<int:group_id>')
