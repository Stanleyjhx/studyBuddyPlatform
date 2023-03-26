from backend.endpoint import utils

GetGroupReqeust = {
    "limit": {
        "type": int,
        "required": True,
    },
    "offset": {
        "type": int,
        "required": True,
    },
    "order_by": {
        "type": str
    },
}


def GetGroupsResponse(number_of_groups, groups):
    return {
        "status": 200,
        "data": {
            "number_of_groups": number_of_groups,
            "groups": groups,
        },
    }


CreateGroupReqeust = {
    "group_name": {
        "type": str,
        "required": True,
    },
    "group_owner": {
        "type": int,
        "required": True,

    },
    "group_description": {
        "type": str,
        "required": True,
    },

}


def CreateGroupResponse(last_row_id):
    return {
        "status": 200,
        "data": {
            "group_id": last_row_id
        }
    }


EditGroupReqeust = {
    "edit_type": {
        "type": utils.EditType,
        "required": True,
    },
    "edit_contents": {
        "type": dict,
        "required": True,
    },
}


def EditGroupResponse():
    return {
        "status": 200,
    }