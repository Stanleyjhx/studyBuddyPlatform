from enum import Enum

table_names = {
    "study_plan": "group_study_plan",
}


class FilterType(Enum):
    FilterByGroupID = 1
    FilterByStudyPlanID = 2


GetStudyPlanReqeust = {
    "group_id": int,
    "study_plan_id": int,
    "filter_type": FilterType,
    "limit": int,
    "offset": int,
}
