

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(user, otp):
    # SMTP server configuration
    smtp_server = 'smtp.gmail.com'  # Update with your SMTP server address
    smtp_port = 465  # Use 465 for SSL

    sender_email = 'tobixdev@gmail.com'  # Update with your sender email address
    sender_password = 'ahbnxwrbwzgaogqa'  # Update with your sender email password
    subject = 'Email Verification'
    body = f'''<div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
   <div style="margin:50px auto;width:70%;padding:20px 0">
     <div style="border-bottom:1px solid #eee">
       <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">Tobix Dev.</a>
     </div>
     <p style="font-size:1.1em">Hi, {user.first_name}</p>
     <p>Welcome. Use the following OTP to complete your Sign Up procedures. OTP is valid for 5 minutes</p>
     <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{otp}</h2>
     <p style="font-size:0.9em;">Regards,<br />Tobix Dev</p>
     <hr style="border:none;border-top:1px solid #eee" />
     <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
       <p>Tobix Inc</p>
     </div>
   </div>
 </div>
 '''  # Update with your email body

    # Create a message container
    msg = MIMEMultipart()
    msg['From'] = 'Tobix Dev. <tobi@tobix.dev>'
    msg['To'] = user.email
    msg['Subject'] = subject

    # Add body to the email
    msg.attach(MIMEText(body, 'html'))

    # Establish a connection to the SMTP server
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, user.email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
