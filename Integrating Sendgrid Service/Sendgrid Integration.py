import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='frommaail@gmail.com',
    to_emails='tomail@gmail.com',
    subject='Sending Registration confirmation mail',
    html_content='<strong>You have been successfully REGISTERED</strong>')
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)