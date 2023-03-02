from flask_restful import reqparse
from enum import Enum

table_names = {
    "groups": "groups",
    "study_plan": "events",
}


class FilterType(Enum):
    FilterByGroupID = 1
    FilterByStudyPlanID = 2


class EditType(Enum):
    Delete = 1
    Edit = 2


def get_parser(params):
    parser = reqparse.RequestParser()
    for param, param_type in params.items():
        parser.add_argument(param, type=param_type)
    return parser
