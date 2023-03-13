from flask_restful import reqparse
from enum import Enum
from backend.database.dao.redis_dao_model import tredis

react_ip = "http://192.168.0.100:3000"

table_names = {
    "groups": "groups",
    "study_plan": "events",
    "group_members": "group_members",
}


class FilterType(Enum):
    FilterByGroupID = 1
    FilterByStudyPlanID = 2


class EditType(Enum):
    Delete = 1
    Edit = 2


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


def get_groups_count_key():
    return "total_groups_count"


def validate_session(session_id) -> any:
    user = tredis.get(get_session_key(session_id))
    return user
