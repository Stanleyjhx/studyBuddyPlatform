from enum import Enum


class EditType(Enum):
    Delete = 1
    Edit = 2


table_names = {
    "groups": "groups",
}

GetGroupReqeust = {
    "limit": int,
    "offset": int,
}

CreateGroupReqeust = {
    "group_name": str,
}

EditGroupReqeust = {
    "group_id": str,
    "edit_type": EditType,
    "edit_contents": dict,
}
