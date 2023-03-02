from flask_restful import reqparse
from enum import Enum

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


def get_parser(params, request_type="get"):
    parser = reqparse.RequestParser()
    for param_name, param_type in params.items():
        parser.add_argument(param_name,
                            type=param_type["type"],
                            required=True if "required" in param_type else False,
                            location="args" if request_type == "get" else ['json', 'values'])
    return parser
