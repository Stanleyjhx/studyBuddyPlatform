from backend.endpoint import utils

GetStudyPlanByGroupReqeust = {
    "order_by": {
        "type": str,
    },
    "limit": {
        "type": int,
        "required": True,
    },
    "offset": {
        "type": int,
        "required": True,
    },
    "show_deleted": {
        "type": bool
    },
}


def GetStudyPlanByGroupResponse(number_of_study_plan, study_plan):
    return {
        "status": 200,
        "data": {
            "number_of_study_plan": number_of_study_plan,
            "study_plan": list(study_plan),
        },
    }



def GetStudyPlanResponse(study_plan, is_a_member):
    return {
        "status": 200,
        "data": {
            "study_plan": study_plan,
            "is_a_member": is_a_member
        },
    }


CreateStudyPlanReqeust = {
    "start_time": {
        "type": str,
    },
    "end_time": {
        "type": str,
        "required": True,
    },
    "capacity": {
        "type": int,
        "required": True,
    },
    "event_name": {
        "type": str,
        "required": True,
    },
    "location": {
        "type": str,
    },
    "description": {
        "type": str
    }
}


def CreateStudyPlanResponse():
    return {
        "status": 200,
    }


EditStudyPlanReqeust = {
    "edit_type": {
        "type": utils.EditType,
        "required": True,
    },
    "edit_contents": {
        "type": dict,
        "required": True,
    }
}


def GetGroupMembersResponse(group_members_info):
    return {
        "status": 200,
        "data": {
            "group_members": group_members_info
        }
    }


def GetEventMembersResponse(event_members_info):
    return {
        "status": 200,
        "data": {
            "event_members": event_members_info
        }
    }
