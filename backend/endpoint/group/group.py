import mysql.connector
from flask_restful import Resource, Api, fields, marshal_with
from backend.database.dao.mysql_dao_model import DAO
from backend.endpoint import utils
from backend.endpoint.group import vars
from flask import Blueprint, current_app, request

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
        groups_dao_object = DAO(table_name=utils.table_names["groups"], logger=current_app.logger)
        cursor = request.cnx.cursor(buffered=True)
        try:
            request.cnx.start_transaction()

            cursor.execute(groups_dao_object.Count(filter_by="is_deleted = 0"))
            total_groups_count = cursor.fetchone()[0]
            request.cnx.commit()
            cursor.close()
            return {
                "status": 200,
                "data": {
                    "number_of_groups": total_groups_count,
                },
            }
        except mysql.connector.Error as err:
            request.cnx.rollback()
            cursor.close()
            return utils.err_response(err)


class GetGroups(Resource):
    @marshal_with(response)
    # fetch groups in a paginated manner
    def get(self):
        args = utils.get_parser(vars.GetGroupReqeust).parse_args()

        order_by = args.get("order_by")
        limit = args.get("limit")
        offset = args.get("offset")
        group_id = args.get("group_id")
        user_id = int(request.user_id)
        show_deleted = False if args.get("show_deleted") is None else bool(args.get("show_deleted"))
        show_mygroup = False if args.get("show_mygroup") is None else bool(args.get("show_mygroup"))

        groups_dao_object = DAO(utils.table_names["groups"], logger=current_app.logger)
        groups_members_object = DAO(utils.table_names["group_members"], logger=current_app.logger)
        cursor = request.cnx.cursor(dictionary=True, buffered=True)

        try:
            request.cnx.start_transaction()
            if group_id is not None:
                group_id_filter = "and group_id = {}".format(group_id)
            elif show_mygroup:
                cursor.execute(groups_members_object.Get(column="group_id",
                                                         filter_by="user_id = {}".format(user_id),
                                                         ))
                group_ids = [str(i['group_id']) for i in cursor.fetchall()]
                group_id_filter = "and group_id in ({})".format(','.join(group_ids))
            else:
                group_id_filter = ""
            cursor.execute(groups_dao_object.GetWithPagination(column="group_id, group_owner, group_name, "
                                                                      "group_description, is_deleted, module_tags",
                                                               filter_by=
                                                               "{} {}".format("is_deleted = 0" if not show_deleted else "1",
                                                                              group_id_filter),
                                                               limit=limit,
                                                               offset=offset,
                                                               order_by=order_by if order_by is not None else "1"))
            groups_info = list(cursor.fetchall())
            group_owners = utils.get_user_info(user_ids=[str(i['group_owner']) for i in groups_info],
                                               logger=current_app.logger,
                                               cursor=cursor)
            cursor.execute(groups_members_object.Get(column="group_id",
                                                     filter_by="user_id={}".format(user_id)))
            user_is_a_member_group = [rows['group_id'] for rows in cursor.fetchall()]
            for group_info in groups_info:
                group_info["group_owner"] = group_owners[str(group_info["group_owner"])]
                group_info["is_a_member"] = True if group_info['group_id'] in user_is_a_member_group else False
            result = vars.GetGroupsResponse(cursor.rowcount, groups_info)
            request.cnx.commit()
            cursor.close()
            request.cnx.close()
            return result

        except mysql.connector.Error as err:
            request.cnx.rollback()
            cursor.close()
            request.cnx.close()
            return utils.err_response(err)


class CreateGroup(Resource):
    @marshal_with(response)
    def post(self):
        # fetch groups in a paginated manner
        args = utils.get_parser(vars.CreateGroupReqeust, "post").parse_args()

        group_name = args.get("group_name")
        token = request.headers.get("Authorization")
        module_tag = request.headers.get("module_tag") if request.headers.get("module_tag") is not None else ''
        user_id = utils.validate_session(token.split()[1])
        group_owner = int(request.user_id)
        group_description = args.get("group_description").replace("'", "\'")

        groups_dao_object = DAO(utils.table_names["groups"], logger=current_app.logger)
        group_member_dao_object = DAO(utils.table_names["group_members"], logger=current_app.logger)
        cursor = request.cnx.cursor(dictionary=True, buffered=True)

        try:
            request.cnx.start_transaction()
            cursor.execute(groups_dao_object.Insert(value={
                "group_name": group_name,
                "group_owner": user_id,
                "module_tags": module_tag,
                "group_description": group_description,
                "is_deleted": 0,
            }))
            cursor.execute(group_member_dao_object.Insert(value={
                "group_id": cursor.lastrowid,
                "user_id": group_owner,
            }))
            result = utils.post_success_response()
            request.cnx.commit()
            cursor.close()
            request.cnx.close()
            return result

        except mysql.connector.Error as err:
            request.cnx.rollback()
            cursor.close()
            request.cnx.close()
            return utils.err_response(err)


class EditGroup(Resource):
    def post(self, group_id):
        # fetch groups in a paginated manner
        args = utils.get_parser(vars.EditGroupReqeust, "post").parse_args()

        edit_contents = args.get("edit_contents")
        edit_type = args.get("edit_type")

        cursor = request.cnx.cursor(dictionary=True)
        groups_dao_object = DAO(utils.table_names["groups"], logger=current_app.logger)

        try:
            request.cnx.start_transaction()

            if edit_type == utils.EditType.Delete:
                cursor.execute(groups_dao_object.Update(value={"is_deleted": "true"},
                                                        filter_by="group_id = {}".format(group_id)))

            elif edit_type == utils.EditType.Edit:
                current_app.logger.info(args.get("edit_contents"))
                cursor.execute(groups_dao_object.Update(value=edit_contents,
                                                        filter_by="group_id = {}".format(group_id)))

            request.cnx.commit()
            cursor.close()
            request.cnx.close()
            return utils.post_success_response()

        except mysql.connector.Error as err:
            request.cnx.rollback()
            cursor.close()
            request.cnx.close()
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
        cnx = mysql.connector.connect(user='sbp',
                                      password='sbp',
                                      host='127.0.0.1',
                                      database='sbp',
                                      pool_size=32)
        cnx.autocommit = False
        setattr(request, "user_id", user_id)
        setattr(request, "cnx", cnx)


@app_group.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
    response.headers['Access-Control-Allow-Credentials'] = "true"
    response.headers['Access-Control-Allow-Method'] = "GET,POST,PUT,DELETE"
    response.headers['Access-Control-Allow-Headers'] = "Origin,Authorization,Content-Type"
    return response


# Group Apis
api_group.add_resource(GetTotalGroupsCount, '/get_total_groups_count')
api_group.add_resource(GetGroups, '/get_groups')
api_group.add_resource(CreateGroup, '/create_group')
api_group.add_resource(EditGroup, '/edit_group/<int:group_id>')
