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
}


def GetStudyPlanByGroupResponse(number_of_study_plan, study_plan):
    return {
        "status": 200,
        "data": {
            "number_of_study_plan": number_of_study_plan,
            "study_plan": list(study_plan),
        },
    }


def GetStudyPlanResponse(study_plan):
    return {
        "status": 200,
        "data": {
            "study_plan": study_plan,
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

GetGroupMembersReqeust = {
    "limit": {
        "type": int,
        "required": True,
    },
    "offset": {
        "type": int,
        "required": True,
    },
}