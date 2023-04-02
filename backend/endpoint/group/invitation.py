import mysql.connector
from flask_restful import Resource, Api, fields, marshal_with
from backend.database.dao.mysql_dao_model import DAO
from backend.endpoint import utils
from backend.endpoint.group import vars
from backend.endpoint.SES.ses_middleware import SesService

from flask import Blueprint, current_app, request

app_invitation = Blueprint(name="app_invitation", import_name="backend.endpoint.route")
api_invitation = Api(app_invitation)

response = {
    'status': fields.Integer,
    'data': fields.Raw,
    'error': fields.String,
}


class Approve(Resource):
    @marshal_with(response)
    # fetch groups in a paginated manner
    def post(self, request_id):
        args = utils.get_parser(vars.ApproveRequest, "post").parse_args()

        status = args.get("status")

        group_request_dao_object = DAO(utils.table_names["group_request"], logger=current_app.logger)
        group_members_dao_object = DAO(utils.table_names["group_members"], logger=current_app.logger)
        cursor = request.cnx.cursor(dictionary=True, buffered=True)

        try:
            request.cnx.start_transaction()
            cursor.execute(group_request_dao_object.Get(column="requester_id, group_id",
                                                        filter_by="membership_request_id = {}".format(request_id)))
            request_info = cursor.fetchone()
            if cursor.rowcount > 0:
                cursor.execute(group_request_dao_object.Update(value={"status": 1 if status == utils.ApprovalStatus.Approve else -1},
                                                               filter_by="membership_request_id = {}".format(
                                                                   request_id)))
                requester_info = utils.get_user_info(user_ids=[str(request_info['requester_id'])],
                                                     logger=current_app.logger,
                                                     cursor=cursor)
                _, group_name = utils.get_group_info(group_ids=request_info['group_id'],
                                                     logger=current_app.logger,
                                                     cursor=cursor)
                if status == utils.ApprovalStatus.Approve:
                    cursor.execute(group_members_dao_object.Insert(value={
                        "group_id": request_info['group_id'],
                        "user_id": requester_info[str(request_info['requester_id'])]['user_id'],
                    }))
                SesService().\
                    send_email_status_update(
                    recipient=requester_info[str(request_info['requester_id'])]['student_id']
                              + '@u.nus.edu',
                    request_info={'entity_type': 'Group',
                                  'entity_name': group_name},
                    status=status
                )
                request.cnx.commit()
                cursor.close()
                request.cnx.close()
                return utils.post_success_response()

            else:
                request.cnx.rollback()
                cursor.close()
                request.cnx.close()
                return utils.err_response("Group request not found")

        except mysql.connector.Error as err:
            request.cnx.rollback()
            cursor.close()
            request.cnx.close()
            return utils.err_response(err)


class Apply(Resource):
    @marshal_with(response)
    # fetch groups in a paginated manner
    def post(self, group_id):
        args = utils.get_parser(vars.ApplyRequest, "post").parse_args()

        apply_reason = args.get("apply_reason")
        requester_id = int(request.user_id)

        group_request_dao_object = DAO(utils.table_names["group_request"], logger=current_app.logger)
        cursor = request.cnx.cursor(dictionary=True, buffered=True)

        try:
            request.cnx.start_transaction()
            group_owner_id, _ = utils.get_group_info(group_ids=str(group_id), logger=current_app.logger, cursor=cursor)
            cursor.execute(group_request_dao_object.Insert(value={
                "group_id": group_id,
                "requester_id": requester_id,
                "apply_reason": apply_reason,
                "group_owner_id": group_owner_id,
            }))
            request.cnx.commit()
            cursor.close()
            request.cnx.close()
            return utils.post_success_response()
        except mysql.connector.Error as err:
            if err.errno == 1062:
                return utils.duplicated_request_response()
            request.cnx.rollback()
            cursor.close()
            request.cnx.close()
            return utils.err_response(err)


class GetRequests(Resource):
    @marshal_with(response)
    # fetch groups in a paginated manner
    def get(self):
        args = utils.get_parser(vars.GetRequestsRequest).parse_args()

        show_role_type = "requester_id" if args.get("role_type") == utils.ApprovalRoleType.Approver else "group_owner_id"
        role_type = "requester_id" if args.get("role_type") != utils.ApprovalRoleType.Approver else "group_owner_id"
        status = args.get("status")
        order_by = args.get("order_by")
        limit = args.get("limit")
        offset = args.get("offset")
        user_id = int(request.user_id)

        group_request_dao_object = DAO(utils.table_names["group_request"], logger=current_app.logger)
        cursor = request.cnx.cursor(dictionary=True, buffered=True)

        try:
            request.cnx.start_transaction()
            cursor.execute(
                group_request_dao_object.GetWithPagination(
                    column="membership_request_id as request_id, group_id, {}, apply_reason, created_at, status, "
                           "DATE_FORMAT(CONVERT_TZ(created_at,'+08:00','+00:00'), '%Y-%m-%dT%H:%i:%s.000Z') "
                           "as created_at".format(show_role_type),
                    filter_by="{} {}".format("{} = {}".format(role_type, user_id),
                                             "and status = {}".format(status) if status is not None else ""),
                    limit=limit,
                    offset=offset,
                    order_by=order_by if order_by is not None else "1"
                )
            )
            requests_info = cursor.fetchall()
            show_roles_info = utils.get_user_info(user_ids=[str(i[show_role_type]) for i in requests_info],
                                                  logger=current_app.logger,
                                                  cursor=cursor)
            groups_info = utils.get_group_info(group_ids=[str(i['group_id']) for i in requests_info],
                                               logger=current_app.logger,
                                               cursor=cursor,
                                               fetch_one=False)
            for request_info in requests_info:
                request_info["group_owner_id"] = show_roles_info[str(request_info[show_role_type])]
                request_info["group_info"] = groups_info[str(request_info['group_id'])]
            request.cnx.commit()
            cursor.close()
            request.cnx.close()
            return vars.GetRequestsResponse(len(requests_info), requests_info, "number_of_requests")

        except mysql.connector.Error as err:
            request.cnx.rollback()
            cursor.close()
            request.cnx.close()
            return utils.err_response(err)


@app_invitation.before_request
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


@app_invitation.after_request
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
    resp.headers['Access-Control-Allow-Credentials'] = "true"
    resp.headers['Access-Control-Allow-Method'] = "GET,POST,PUT,DELETE"
    resp.headers['Access-Control-Allow-Headers'] = "Content-Type,Authorization,Origin"
    return resp


# Invitation Apis
api_invitation.add_resource(Approve, '/approve/<int:request_id>')
api_invitation.add_resource(Apply, '/apply/<int:group_id>')
api_invitation.add_resource(GetRequests, '/get_requests')
