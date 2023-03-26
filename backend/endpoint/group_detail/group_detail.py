import mysql.connector
from flask_restful import Resource, Api, fields, marshal_with
from backend.database.dao.mysql_dao_model import DAO
from backend.endpoint import utils
from backend.endpoint.group_detail import vars

from flask import Blueprint, current_app, request

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
        show_deleted = False if args.get("show_deleted") is None else bool(args.get("show_deleted"))
        user_id = int(request.user_id)

        cursor = request.cnx.cursor(dictionary=True, buffered=True)
        study_plan_dao_object = DAO(utils.table_names["study_plan"], logger=current_app.logger, cursor=cursor)
        event_attendees_dao_object = DAO(table_name=utils.table_names["event_attendees"],
                                         logger=current_app.logger)


        try:
            request.cnx.start_transaction()
            cursor.execute(study_plan_dao_object.GetWithPagination(
                column="event_id, group_id, event_holder, event_name, location, capacity, event_description, is_deleted,"
                       "DATE_FORMAT(CONVERT_TZ(start_time,'+08:00','+00:00'), '%Y-%m-%dT%H:%i:%s.000Z') as start_time,"
                       "DATE_FORMAT(CONVERT_TZ(end_time,'+08:00','+00:00'), '%Y-%m-%dT%H:%i:%s.000Z') as end_time",
                filter_by="group_id = {} and {}".format(group_id, "is_deleted = 0" if not show_deleted else "1"),
                order_by=order_by if order_by is not None else "1",
                limit=limit,
                offset=offset,
            ))
            study_plans = cursor.fetchall()
            event_holders_info = utils.get_user_info(user_ids=[str(i['event_holder']) for i in list(study_plans)],
                                                     logger=current_app.logger,
                                                     cursor=cursor)
            for idx, study_plan in enumerate(study_plans):
                event_holder_id = str(study_plan['event_holder'])
                if event_holder_id in event_holders_info:
                    study_plan['event_holder'] = event_holders_info[event_holder_id]
                else:
                    study_plan['event_holder'] = {"user_id": event_holder_id}
            cursor.execute(event_attendees_dao_object.Get(
                column="event_id",
                filter_by="attendee_id = {}".format(user_id)
            ))
            attendee_is_a_member_study_plan = [rows['event_id'] for rows in cursor.fetchall()]
            for study_plan in study_plans:
                study_plan['is_a_member'] = True if study_plan['event_id'] in attendee_is_a_member_study_plan else False
            request.cnx.commit()
            cursor.close()
            request.cnx.close()
            return vars.GetStudyPlanByGroupResponse(len(study_plans), study_plans)
        except mysql.connector.Error as err:
            request.cnx.rollback()
            cursor.close()
            request.cnx.close()
            return utils.err_response("MySQL facing error : {}".format(err))


class GetStudyPlanById(Resource):
    @marshal_with(response)
    # fetch groups in a paginated manner
    def get(self, study_plan_id):
        user_id = int(request.user_id)
        cursor = request.cnx.cursor(dictionary=True, buffered=True)
        groups_dao_object = DAO(table_name=utils.table_names["study_plan"],
                                logger=current_app.logger)
        event_attendees_dao_object = DAO(table_name=utils.table_names["event_attendees"],
                                         logger=current_app.logger)

        try:
            request.cnx.start_transaction()
            cursor.execute(groups_dao_object.Get(
                column="event_id, group_id, event_holder, event_name, location, capacity, event_description, is_deleted,"
                       "DATE_FORMAT(CONVERT_TZ(start_time,'+08:00','+00:00'), '%Y-%m-%dT%H:%i:%s.000Z') as start_time,"
                       "DATE_FORMAT(CONVERT_TZ(end_time,'+08:00','+00:00'), '%Y-%m-%dT%H:%i:%s.000Z') as end_time",
                filter_by="event_id = {}".format(study_plan_id)
            ))
            request.cnx.commit()
            if cursor.rowcount == 0:
                cursor.close()
                request.cnx.close()
                return utils.err_response("Study Plan {} doesn't exist".format(study_plan_id))
            else:
                result = cursor.fetchone()
                event_holders_info = utils.get_user_info(user_ids=[result['event_holder']],
                                                         logger=current_app.logger,
                                                         cursor=cursor)
                if result['event_holder'] == user_id:
                    is_a_member = True
                else:
                    cursor.execute(
                        event_attendees_dao_object.Get(column="1",
                                                       filter_by="event_id={} and attendee_id={}".format(study_plan_id,
                                                                                                         user_id))
                    )
                    is_a_member = True if cursor.rowcount > 0 else False
                result['event_holder'] = event_holders_info[result['event_holder']]
                cursor.close()
                request.cnx.close()
                return vars.GetStudyPlanResponse(result, is_a_member)

        except mysql.connector.Error as err:
            request.cnx.rollback()
            cursor.close()
            request.cnx.close()
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

        dao_object = DAO(utils.table_names["study_plan"], logger=current_app.logger)
        event_attendees_dao_object = DAO(utils.table_names["event_attendees"], logger=current_app.logger)
        cursor = request.cnx.cursor(dictionary=True)

        try:
            request.cnx.start_transaction()
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
            cursor.execute(event_attendees_dao_object.Insert(value={
                "event_id": cursor.lastrowid,
                "attendee_id": user_id,
                "is_deleted": 0,
            }))
            request.cnx.commit()
            cursor.close()
            request.cnx.close()
            return vars.CreateStudyPlanResponse()

        except mysql.connector.Error as err:
            request.cnx.rollback()
            cursor.close()
            request.cnx.close()
            return utils.err_response(err)


class EditStudyPlan(Resource):
    @marshal_with(response)
    # fetch groups in a paginated manner
    def post(self, study_plan_id):
        args = utils.get_parser(vars.EditStudyPlanReqeust, "post").parse_args()

        edit_type = args.get("edit_type")
        edit_contents = args.get("edit_contents")
        user_id = int(request.user_id)

        study_plan_dao_object = DAO(utils.table_names["study_plan"], logger=current_app.logger)
        cursor = request.cnx.cursor(dictionary=True, buffered=True)

        try:
            request.cnx.start_transaction()

            cursor.execute(
                study_plan_dao_object.Get(column="event_holder", filter_by="event_id = {}".format(study_plan_id)))
            # if cursor.fetchone()["event_holder"] != user_id:
            #     cnx.rollback()
            #     cursor.close()
            #     return utils.lack_permission_response(user_id)
            if edit_type == utils.EditType.Delete:
                cursor.execute(study_plan_dao_object.Update(value={"is_deleted": "1"},
                                                            filter_by="event_id = {}".format(study_plan_id)))
            elif edit_type == utils.EditType.Edit:
                current_app.logger.info(args.get("edit_contents"))
                cursor.execute(study_plan_dao_object.Update(value=edit_contents,
                                                            filter_by="event_id = {}".format(study_plan_id)))

            request.cnx.commit()
            cursor.close()
            request.cnx.close()
            return vars.CreateStudyPlanResponse()

        except mysql.connector.Error as err:
            request.cnx.rollback()
            cursor.close()
            request.cnx.close()
            return utils.err_response(err)


class GetGroupMembers(Resource):
    @marshal_with(response)
    # fetch groups in a paginated manner
    def get(self, group_id):
        group_members_dao_object = DAO(utils.table_names["group_members"], logger=current_app.logger)
        cursor = request.cnx.cursor(dictionary=True, buffered=True)

        try:
            request.cnx.start_transaction()
            cursor.execute(group_members_dao_object.Get(column="user_id", filter_by="group_id = {}".format(group_id)))
            group_members_id = [str(i['user_id']) for i in list(cursor.fetchall())]
            group_members_info = []
            if len(group_members_id) != 0:
                group_members_info = utils.get_user_info(group_members_id, logger=current_app.logger, cursor=cursor)
                group_members_info = [v for k, v in group_members_info.items()]
            request.cnx.commit()
            cursor.close()
            request.cnx.close()
            return vars.GetGroupMembersResponse(group_members_info)

        except mysql.connector.Error as err:
            request.cnx.rollback()
            cursor.close()
            request.cnx.close()
            return utils.err_response(err)


class GetEventMembers(Resource):
    @marshal_with(response)
    # fetch groups in a paginated manner
    def get(self, study_plan_id):
        group_members_dao_object = DAO(utils.table_names["event_attendees"], logger=current_app.logger)
        cursor = request.cnx.cursor(dictionary=True, buffered=True)
        try:
            request.cnx.start_transaction()
            cursor.execute(group_members_dao_object.Get(column="attendee_id",
                                                        filter_by="event_id = {}".format(study_plan_id)))
            event_members_id = [str(i['attendee_id']) for i in list(cursor.fetchall())]
            event_members_info = []
            if len(event_members_id) != 0:
                event_members_info = utils.get_user_info(event_members_id, logger=current_app.logger, cursor=cursor)
                event_members_info = [v for k, v in event_members_info.items()]
            request.cnx.commit()
            cursor.close()
            request.cnx.close()
            return vars.GetEventMembersResponse(event_members_info)

        except mysql.connector.Error as err:
            request.cnx.rollback()
            cursor.close()
            request.cnx.close()
            return utils.err_response(err)


class AddEventMember(Resource):
    @marshal_with(response)
    # fetch groups in a paginated manner
    def post(self, study_plan_id):
        user_id = int(request.user_id)
        group_members_dao_object = DAO(utils.table_names["event_attendees"], logger=current_app.logger)
        cursor = request.cnx.cursor(dictionary=True, buffered=True)
        try:
            request.cnx.start_transaction()
            cursor.execute(group_members_dao_object.Insert(value={
                "event_id": study_plan_id,
                "attendee_id": user_id,
                "is_deleted": 0,
            }))
            request.cnx.commit()
            cursor.close()
            request.cnx.close()
            return utils.post_success_response()

        except mysql.connector.Error as err:
            request.cnx.rollback()
            cursor.close()
            request.cnx.close()
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
        cnx = mysql.connector.connect(user='sbp',
                                      password='sbp',
                                      host='127.0.0.1',
                                      database='sbp',
                                      pool_size=32)
        cnx.autocommit = False
        setattr(request, "user_id", user_id)
        setattr(request, "cnx", cnx)


@app_group_detail.after_request
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
    resp.headers['Access-Control-Allow-Credentials'] = "true"
    resp.headers['Access-Control-Allow-Method'] = "GET,POST,PUT,DELETE"
    resp.headers['Access-Control-Allow-Headers'] = "Content-Type,Authorization,Origin"
    return resp


# Group Detail Apis
api_group_detail.add_resource(GetStudyPlanByGroup, '/get_study_plan_by_group/<int:group_id>')
api_group_detail.add_resource(GetStudyPlanById, '/get_study_plan_by_id/<int:study_plan_id>')
api_group_detail.add_resource(CreateStudyPlan, '/create_study_plan/<int:group_id>')
api_group_detail.add_resource(EditStudyPlan, '/edit_study_plan/<int:study_plan_id>')
api_group_detail.add_resource(GetGroupMembers, '/get_group_members/<int:group_id>')
api_group_detail.add_resource(GetEventMembers, '/get_event_members/<int:study_plan_id>')
api_group_detail.add_resource(AddEventMember, '/add_event_member/<int:study_plan_id>')
