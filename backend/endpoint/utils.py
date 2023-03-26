from flask_restful import reqparse
from enum import Enum
from backend.database.dao.redis_dao_model import tredis
from backend.database.dao.mysql_dao_model import DAO

react_ip = "http://172.20.10.10:3000"

table_names = {
    "groups": "groups",
    "study_plan": "events",
    "group_members": "group_members",
    "users": "users",
    "group_request": "membership_requests",
    "event_attendees": "event_attendees",
}


class EditType(Enum):
    Delete = 1
    Edit = 2


class ApprovalStatus(Enum):
    Decline = -1
    Approve = 1


class ApprovalRoleType(Enum):
    Requester = '1'
    Approver = '2'


def err_response(err):
    return {
        "status": 400,
        "error": "{}".format(str(err)),
    }


def unauthenticated_response():
    return {
        "status": 401,
        "error": "Unauthenticated User"
    }


def post_success_response():
    return {
        "status": 200,
    }


def lack_permission_response(user_id):
    return {
        "status": 403,
        "error": "User {} does not have permission".format(user_id)
    }


def get_parser(params, request_type="get"):
    parser = reqparse.RequestParser()
    for param_name, param_type in params.items():
        parser.add_argument(param_name,
                            type=param_type["type"],
                            required=True if "required" in param_type else False,
                            location="args" if request_type == "get" else ['json', 'values'])
    return parser


def get_session_key(uuid):
    return "session_id_{}".format(uuid)


def get_user_info_key(user_id):
    return "user_id_{}".format(user_id)


def get_groups_count_key():
    return "total_groups_count"


def get_group_info_key(group_id):
    return "group_id_{}".format(group_id)


def validate_session(session_id) -> any:
    user = tredis.get(get_session_key(session_id))
    return user


def get_user_info(user_ids, logger, cursor):
    user_ids_not_in_redis = []
    user_info = {}
    user_dao_object = DAO(table_name=table_names["users"],
                          logger=logger)
    for user_id in user_ids:
        user_info_redis = tredis.hgetall(get_user_info_key(user_id))
        if len(user_info_redis) == 0:
            user_ids_not_in_redis.append(user_id)
        else:
            user_info[user_id] = user_info_redis

    if len(user_ids_not_in_redis) > 0:
        cursor.execute(user_dao_object.Get(column="user_id, user_name, first_name, last_name, student_id,"
                                                  "major, description",
                                           filter_by="user_id in ({})".
                                           format(",".join(user_ids_not_in_redis))))

        for user_info_not_in_redis in list(cursor.fetchall()):
            user_info[user_info_not_in_redis['user_id']] = user_info_not_in_redis
            tredis.hmset(get_user_info_key(user_info_not_in_redis['user_id']), user_info_not_in_redis)

    return user_info


def get_group_info(group_ids, logger, cursor, fetch_one=True):
    group_dao_object = DAO(table_name=table_names["groups"],
                           logger=logger)
    group_info = {}
    if fetch_one:
        group_info = tredis.hgetall(get_group_info_key(group_ids))
        if group_info == {}:
            cursor.execute(group_dao_object.Get(column="group_id,group_owner, group_name",
                                                filter_by="group_id = {}".format(group_ids)))
            result = cursor.fetchone()
            group_info['group_owner'] = result['group_owner']
            group_info['group_name'] = result['group_name']
            logger.info(group_info)
            tredis.hmset(get_group_info_key(group_ids), dict(group_info))
        return group_info['group_owner'], group_info['group_name']
    else:
        group_ids_not_in_redis = []
        for group_id in group_ids:
            group_info_redis = tredis.hgetall(get_group_info_key(group_id))
            if group_info_redis == {}:
                group_ids_not_in_redis.append(group_id)
            else:
                group_info[group_id] = group_info_redis

        if len(group_ids_not_in_redis) > 0:
            cursor.execute(group_dao_object.Get(column="group_owner, group_name, group_id",
                                                filter_by="group_id in ({})".format(','.join(group_ids))))
        for group_id_in_redis in list(cursor.fetchall()):
            group_info[group_id_in_redis['group_id']] = group_id_in_redis
            tredis.hmset(get_group_info_key(group_id_in_redis['group_id']), dict(group_id_in_redis))
        return group_info


def duplicated_request_response():
    return {
        "status": 300,
        "error": "Duplicated Request",
    }
