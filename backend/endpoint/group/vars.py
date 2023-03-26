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
    "show_deleted": {
        "type": bool
    },
    "group_id": {
        "type": int,
    },
    "show_mygroup": {
        "type": bool,
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
    "group_description": {
        "type": str,
        "required": True,
    },
    "module_tag": {
        "type": str
    },

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


ApproveRequest = {
    "status": {
        "type": utils.ApprovalStatus,
        "required": True,
    }
}

ApplyRequest = {
    "apply_reason": {
        "type": str,
        "required": True,
    }
}

GetRequestsRequest = {
    "role_type": {
        "type": utils.ApprovalRoleType,
        "required": True,
    },
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
    "status": {
        "type": utils.ApprovalStatus,
    }
}


def GetRequestsResponse(number_of_requests, requests, title="number_of_groups"):
    return {
        "status": 200,
        "data": {
            title: number_of_requests,
            "requests": requests,
        },
    }
