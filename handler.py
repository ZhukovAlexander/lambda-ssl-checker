import socket
import ssl
import datetime
import json

import boto3


def ssl_valid_time_remaining(hostname):
    """Get the number of days left in a cert's lifetime."""
    expires = ssl_expiry_datetime(hostname)
    return expires - datetime.datetime.utcnow()

def ssl_expires_in(hostname, buffer_days=14):
    """Check if `hostname` SSL cert expires is within `buffer_days`.

    Raises `AlreadyExpired` if the cert is past due
    """
    remaining = ssl_valid_time_remaining(hostname)

    # if the cert expires in less than two weeks, we should reissue it
    if remaining < datetime.timedelta(days=0):
        # cert has already expired - uhoh!
        raise AlreadyExpired("Cert expired %s days ago" % remaining.days)
    elif remaining < datetime.timedelta(days=buffer_days):
        # expires sooner than the buffer
        return True, remaining
    else:
        # everything is fine
        return False, remaining

def ssl_expiry_datetime(hostname):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )

    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()
    return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)

def lambda_handler(event, context):
    domain = event['domain']
    if_expires_in = event['if_expires_in']
    status, expires_in = ssl_expires_in(domain, if_expires_in)
    if status or 1:
        sns = boto3.client('sns')
        ACCOUNT_ID = context.invoked_function_arn.split(":")[4] # hack
        sns.publish(
            TopicArn='arn:aws:sns:us-east-1:{}:SSLExpiryAlerts'.format(ACCOUNT_ID),
            Message=json.dumps({'domain': domain, "expires": expires_in.days})
        )
    return 'SSL certificate for {} expires in {} days'.format(domain, expires_in.days)
