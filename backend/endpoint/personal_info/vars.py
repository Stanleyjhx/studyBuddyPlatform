from backend.endpoint import utils

EditPersonalInfoReqeust = {
    "edit_type": {
        "type": utils.EditType,
        "required": True,
    },
    "edit_contents": {
        "type": dict,
        "required": True,
    }
}


def EditPersonalInfoResponse():
    return {
        "status": 200,
    }


def GetPersonalInfoResponse(personal_info):
    return {
        "status": 200,
        "data": {
            "personal_info": personal_info,
        },
    }
