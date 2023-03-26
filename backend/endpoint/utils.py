from flask_restful import reqparse
from enum import Enum
from backend.database.dao.redis_dao_model import tredis
from backend.endpoint.register import vars

import boto3
import random
import configparser
import re

react_ip = "http://172.20.10.10:3000"

table_names = {
    "groups": "`groups`",
    "study_plan": "events",
    "group_members": "group_members",
    "users": "users"
}


class FilterType(Enum):
    FilterByGroupID = 1
    FilterByStudyPlanID = 2
    FilterByUserID = 3


class EditType(Enum):
    Delete = 1
    Edit = 2


def err_response(err):
    return {
        "status": 400,
        "error": "{}".format(str(err)),
    }


def unauthenticated_response():
    return {
        "status": 401,
        "error": "Unauthenticated User"
    }


def lack_permission_response(user_id):
    return {
        "status": 403,
        "error": "User {} does not have permission".format(user_id)
    }


def invalid_email_format_response():
    return {
        "status": 403,
        "error": "Please check the format/domain of your email address."
    }


def get_parser(params, request_type="get"):
    parser = reqparse.RequestParser()
    for param_name, param_type in params.items():
        parser.add_argument(param_name,
                            type=param_type["type"],
                            required=True if "required" in param_type else False,
                            location="args" if request_type == "get" else ['json', 'values'])
    return parser


def get_session_key(uuid):
    return "session_id_{}".format(uuid)


def get_groups_count_key():
    return "total_groups_count"


def get_user_id():
    return "user_id"


def validate_session(session_id) -> any:
    user = tredis.get(get_session_key(session_id))
    return user


def check_email_format(addr):
    """
    Check the email validity as well as NUS domain.
    :param addr:
    :return: boolean
    """
    if not addr.endswith(('nus.edu', 'nus.edu.sg')):
        return False
    else:
        pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
        return re.match(pattern=pattern, string=addr) is not None


def generate_verification_code():
    return str(random.randint(100000, 999999))


def send_verification_email(email, verification_code):
    config = configparser.ConfigParser()
    config.read('./config.ini')
    subject, body_html, _ = vars.verification_email_template(verification_code)
    ses_client = boto3.client(
        'ses',
        aws_access_key_id=config['aws']['access_key'],
        aws_secret_access_key=config['aws']['secret_key'],
        region_name=config['aws']['region']
    )
    # subject = "Greetings from nexus"
    # body_html = """
    #
    #             """ + url

    try:
        response = ses_client.send_email(
            Source='e0950215@u.nus.edu',
            Destination={
                'ToAddresses': [
                    email
                ]
            },
            Message={
                'Subject': {
                    'Charset': 'utf-8',
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Charset': 'utf-8',
                        'Data': body_html
                    },
                    'Html': {
                        'Charset': 'utf-8',
                        'Data': body_html
                    }
                }
            }
        )
        return response['ResponseMetadata']['HTTPStatusCode']
    except Exception as e:
        return e
