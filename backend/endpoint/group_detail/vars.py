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
            "study_plan": study_plan,
        },
    }


def GetStudyPlanResponse(study_plan):
    return {
        "status": 200,
        "data": {
            "study_plan": study_plan,
        },
    }
