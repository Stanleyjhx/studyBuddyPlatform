from botocore.exceptions import ClientError, WaiterError
from .vars import verification_email_template,request_result_email_template
import boto3


class SesService:
    def __init__(self, logger):
        self.ses_client = boto3.client('ses', region_name="ap-southeast-1")
        self.logger = logger

    def verify_email_identity(self, email_address):
        try:
            self.ses_client.verify_email_identity(EmailAddress=email_address)
            self.logger.info("Started verification of %s.", email_address)
        except ClientError:
            self.logger.exception("Couldn't start verification of %s.", email_address)
            raise

    def wait_until_identity_exists(self, identity):
        try:
            waiter = self.ses_client.get_waiter('identity_exists')
            self.logger.info("Waiting until %s exists.", identity)
            waiter.wait(Identities=[identity])
            return True
        except WaiterError:
            self.logger.error("Waiting for identity %s failed or timed out.", identity)
            return False

    def send_email_verification(self, recipient, token, configure_set=''):
        sender = "NEXUS <nexus.study.platform@gmail.com>"
        charset = "UTF-8"
        client = boto3.client('ses', region_name="ap-southeast-1")
        subject, body_html, _ = verification_email_template(token)
        try:
            response = client.send_email(
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
            self.logger.info(e.response['Error']['Message'])
        else:
            self.logger.info("Email sent! Message ID: {}".format(response['MessageId']))

    def send_email_status_update(self, recipient, request_info, status):
        sender = "NEXUS <nexus.study.platform@gmail.com>"
        charset = "UTF-8"
        client = boto3.client('ses', region_name="ap-southeast-1")
        subject, body_html, body_text = request_result_email_template(request_info=request_info,
                                                                      status=status)
        try:
            response = client.send_email(
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
            self.logger.info(e.response['Error']['Message'])
            return False
        else:
            self.logger.info("Email sent! Message ID: {}".format(response['MessageId']))
            return True
