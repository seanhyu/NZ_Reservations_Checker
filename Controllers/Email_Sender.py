import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from configs import SENDGRID_KEY, FROM_EMAIL


# this function attempts to send an email to the corresponding user if their specified itinerary is available

def send_email(email,track,month,day,year,size) -> bool:
    # draft contents of email
    email_content = f"""<strong>Congratulations! There is a spot available for the {track} on {month}/{day}/{year} for {size} hiker(s)!</strong>""" 

    # drafts the email    
    message = Mail(
        from_email= FROM_EMAIL,
        to_emails=email,
        subject='NZ Great Walks Spot Available!',
        html_content=email_content)
    
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
    
