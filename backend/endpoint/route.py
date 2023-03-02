from flask import Flask, request
from flask_restful import Resource, Api, fields, marshal_with
from backend.endpoint.group import group
from backend.endpoint.group_detail import group_detail

app = Flask(__name__)
api = Api(app)

# Group Apis
api.add_resource(group.GetTotalGroupsCount, '/get_total_groups_count')
api.add_resource(group.GetGroups, '/get_groups')
api.add_resource(group.CreateGroup, '/create_group')
api.add_resource(group.EditGroup, '/edit_group/<int:group_id>')

# Group Detail Apis
api.add_resource(group_detail.GetStudyPlanByGroup, '/get_study_plan_by_group/<int:group_id>')
api.add_resource(group_detail.GetStudyPlan, '/get_study_plan/<int:study_plan_id>')

if __name__ == '__main__':
    app.run(debug=True)

