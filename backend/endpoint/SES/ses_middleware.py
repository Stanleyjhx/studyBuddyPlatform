from botocore.exceptions import ClientError, WaiterError
from .vars import verification_email_template,request_result_email_template
import boto3
import os


class SesService:
    def __init__(self):
        self.ses_client = boto3.client('ses', region_name="ap-southeast-1")

    def verify_email_identity(self, email_address):
        try:
            self.ses_client.verify_email_identity(EmailAddress=email_address)
            #self.logger.info("Started verification of %s.", email_address)
        except ClientError:
            #self.logger.exception("Couldn't start verification of %s.", email_address)
            raise

    def wait_until_identity_exists(self, identity):
        try:
            waiter = self.ses_client.get_waiter('identity_exists')
            waiter.wait(Identities=[identity])
            return True
        except WaiterError:
            return False

    def send_email_verification(self, recipient, token, configure_set=''):
        sender = "NEXUS <nexus.study.platform@gmail.com>"
        charset = "UTF-8"
        subject, body_html, _ = verification_email_template(token)
        try:
            response = self.ses_client.send_email(
                Destination={
                    'ToAddresses': [
                        recipient,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': charset,
                            'Data': body_html,
                        },
                        'Text': {
                            'Charset': charset,
                            'Data': body_html,
                        },
                    },
                    'Subject': {
                        'Charset': charset,
                        'Data': subject,
                    },
                },
                Source=sender,
            )
        except ClientError as e:
            return e.response['Error']['Message']
        else:
            return response['ResponseMetadata']['HTTPStatusCode']

    def send_email_status_update(self, recipient, request_info, status):
        sender = "NEXUS <nexus.study.platform@gmail.com>"
        charset = "UTF-8"
        subject, body_html, body_text = request_result_email_template(request_info=request_info,
                                                                      status=status)
        try:
            response = self.ses_client.send_email(
                Destination={
                    'ToAddresses': [
                        recipient,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': charset,
                            'Data': body_html,
                        },
                        'Text': {
                            'Charset': charset,
                            'Data': body_html,
                        },
                    },
                    'Subject': {
                        'Charset': charset,
                        'Data': subject,
                    },
                },
                Source=sender,
            )
        except ClientError as e:
            #self.logger.info(e.response['Error']['Message'])
            return False
        else:
            #self.logger.info("Email sent! Message ID: {}".format(response['MessageId']))
            return response['ResponseMetadata']['HTTPStatusCode']
