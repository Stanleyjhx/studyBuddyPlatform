from backend.endpoint import utils

GetGroupReqeust = {
    "show_deleted": bool,
    "limit": int,
    "offset": int,
    "order_by": str,
}

CreateGroupReqeust = {
    "group_name": str,
}

EditGroupReqeust = {
    "group_id": str,
    "edit_type": utils.EditType,
    "edit_contents": dict,
}
