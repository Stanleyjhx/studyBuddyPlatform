from flask_restful import reqparse
from enum import Enum
from ..database.dao.redis_dao_model import tredis
from .register import vars
import boto3
import random
import configparser
import re

react_ip = "http://172.20.10.10:3000"


class FilterType(Enum):
    FilterByGroupID = 1
    FilterByStudyPlanID = 2
    FilterByUserID = 3


from ..database.dao.mysql_dao_model import DAO

table_names = {
    "groups": "`groups`",
    "study_plan": "events",
    "group_members": "group_members",
    "users": "users",
    "group_request": "membership_requests",
    "event_attendees": "event_attendees",
}


class EditType(Enum):
    Delete = 1
    Edit = 2


class ApprovalStatus(Enum):
    Decline = -1
    Approve = 1


class ApprovalRoleType(Enum):
    Requester = '1'
    Approver = '2'


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


def post_success_response():
    return {
        "status": 200,
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


def get_user_info_key(user_id):
    return "user_id_{}".format(user_id)


def get_groups_count_key():
    return "total_groups_count"


def get_user_id():
    return "user_id"


def get_group_info_key(group_id):
    return "group_id_{}".format(group_id)


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


def get_user_info(user_ids, logger, cursor):
    user_ids_not_in_redis = []
    user_info = {}
    user_dao_object = DAO(table_name=table_names["users"],
                          logger=logger)
    for user_id in user_ids:
        user_info_redis = tredis.hgetall(get_user_info_key(user_id))
        if len(user_info_redis) == 0:
            user_ids_not_in_redis.append(user_id)
        else:
            user_info[user_id] = user_info_redis

    if len(user_ids_not_in_redis) > 0:
        cursor.execute(user_dao_object.Get(column="user_id, user_name, first_name, last_name, student_id,"
                                                  "major, description",
                                           filter_by="user_id in ({})".
                                           format(",".join(user_ids_not_in_redis))))

        for user_info_not_in_redis in list(cursor.fetchall()):
            user_info[user_info_not_in_redis['user_id']] = user_info_not_in_redis
            tredis.hmset(get_user_info_key(user_info_not_in_redis['user_id']), user_info_not_in_redis)

    return user_info


def get_group_info(group_ids, logger, cursor, fetch_one=True):
    group_dao_object = DAO(table_name=table_names["groups"],
                           logger=logger)
    group_info = {}
    if fetch_one:
        group_info = tredis.hgetall(get_group_info_key(group_ids))
        if group_info == {}:
            cursor.execute(group_dao_object.Get(column="group_id,group_owner, group_name",
                                                filter_by="group_id = {}".format(group_ids)))
            result = cursor.fetchone()
            group_info['group_owner'] = result['group_owner']
            group_info['group_name'] = result['group_name']
            logger.info(group_info)
            tredis.hmset(get_group_info_key(group_ids), dict(group_info))
        return group_info['group_owner'], group_info['group_name']
    else:
        group_ids_not_in_redis = []
        for group_id in group_ids:
            group_info_redis = tredis.hgetall(get_group_info_key(group_id))
            if group_info_redis == {}:
                group_ids_not_in_redis.append(group_id)
            else:
                group_info[group_id] = group_info_redis

        if len(group_ids_not_in_redis) > 0:
            cursor.execute(group_dao_object.Get(column="group_owner, group_name, group_id",
                                                filter_by="group_id in ({})".format(','.join(group_ids))))
        for group_id_in_redis in list(cursor.fetchall()):
            group_info[group_id_in_redis['group_id']] = group_id_in_redis
            tredis.hmset(get_group_info_key(group_id_in_redis['group_id']), dict(group_id_in_redis))
        return group_info


def duplicated_request_response():
    return {
        "status": 300,
        "error": "Duplicated Request",
    }
