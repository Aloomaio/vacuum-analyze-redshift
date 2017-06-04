
import analyze_vacuum_schema
import os
import sys
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders
from email.mime.text import MIMEText


def parse_args():
    """
    Parsing the required arguments to establish a database connection.
    """

    # hardcoded arguments to be parsed
    db_arguments = [('--db', 'DB_NAME', True),
                    ('--db-user', 'DB_USER', True),
                    ('--db-pwd', 'DB_PWD', True),
                    ('--db-host', 'DB_HOST', True),
                    ('--schema-name', 'DB_SCHEMA', False),
                    ('--table-name', 'DB_TABLE', False),
                    ('--output-file', 'OUTPUT_FILE', True),
                    ('--debug', 'DEBUG', False),
                    ('--slot-count', 'SLOT_COUNT', False),
                    ('--ignore-errors', 'IGNORE_ERRORS', False),
                    ('--analyze-flag', 'ANALYZE_FLAG', False),
                    ('--vacuum-flag', 'VACUUM_FLAG', False),
                    ('--vacuum-parameter', 'VACUUM_PARAM', False),
                    ('--min-unsorted-pct', 'MIN_UNSORTED_PCT', False),
                    ('--max-unsorted-pct', 'MAX_UNSORTED_PCT', False),
                    ('--deleted-pct', 'DELETED_PCT', False),
                    ('--stats-off-pct', 'STATS_OFF_PCT', False),
                    ('--max-table-size-mb', 'MAX_TABLE_SIZE_MB', False)]

    # place holder for argv[0] - to be trimmed by the aws script
    argv = [(None)]

    # build arguments list to send to aws script
    for tup in db_arguments:
        if tup[2] == True:
            if tup[1] not in os.environ:
                print('Missing %s - mandatory argument.' % (tup[1]))
                sys.exit(2)
            else:
                argv.append(tup[0])
                argv.append(os.environ[tup[1]])
        else:
            if tup[1] in os.environ:
                argv.append(tup[0])
                argv.append(os.environ[tup[1]])
    return argv


def send_email():
    """
    Sending the log results in an email message, if all the e-mail credentials are provided
    """

    email_arguments = ['EMAIL_HOST',
                       'EMAIL_PORT',
                       'EMAIL_SENDER',
                       'EMAIL_PWD',
                       'EMAIL_RECIPIENT']


    for arg in email_arguments:
        if arg not in os.environ:
            print('Missing %s - mandatory argument for e-mail report.' % (arg))
            sys.exit(2)

    sender = os.environ['EMAIL_SENDER']
    recipient = os.environ['EMAIL_RECIPIENT']
    try:
        s = smtplib.SMTP(host=os.environ['EMAIL_HOST'],
                         port=os.environ['EMAIL_PORT'])
    except smtplib.SMTPConnectError as e:
        print("Connection failed: wrong credentials for SMTP {0}:{1}".format(os.environ['EMAIL_HOST'], os.environ['EMAIL_PORT']))
        sys.exit(2)
    s.starttls()
    try:
        s.login(sender, os.environ['EMAIL_PWD'])
    except smtplib.SMTPAuthenticationError as e:
        print("Connection failed: wrong username or password -> {0}@{1}".format(os.environ['EMAIL_SENDER'], os.environ['EMAIL_PWD']))
        sys.exit(2)
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = "Your VACUUM/ANALYZE Report is ready!"

    # attach the log file
    part = MIMEBase('application', 'octet-stream')
    try:
        file = open(os.environ['OUTPUT_FILE'], 'rb')
        part.set_payload(file.read())
        Encoders.encode_base64(part)
        part.add_header('content-disposition',
                        'attachment; filename = "log.txt"')
        msg.attach(part)
        msg.attach(
            MIMEText('Please see the attached file for your log.', 'plain'))
    except (OSError, IOError) as e:
        msg.attach(MIMEText('Attaching the log has failed.\n {0}: {1}'.format(
            e.errno, e.strerror), 'plain'))

    s.sendmail(sender, recipient, msg.as_string())
    del msg
    s.quit


if __name__ == '__main__':
    argv = parse_args()
    analyze_vacuum_schema.main(argv)
    if (os.environ['SEND_EMAIL'] == 'True'):
        send_email()
