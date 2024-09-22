import os
from Configs import SENDGRID_KEY, FROM_EMAIL
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# this function attempts to send an email to the corresponding user if their specified itinerary is available

def send_email(email) -> bool:

    # drafts the email    
    message = Mail(
        from_email= FROM_EMAIL,
        to_emails=email,
        subject='NZ Great Walks Spot Available!',
        html_content='<strong>There is a spot available for your specified itinerary!</strong>')
    
    # attempts to send the email
    try:
        sg = SendGridAPIClient(os.environ.get(SENDGRID_KEY)) # Create and enter your own SendGrid key here
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return True
    except Exception as e:
        print("Failed to send email", e)
        return False