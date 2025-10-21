import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Email account credentials
sender_email = 'shankershawn@gmail.com'
receiver_email = 'shankarsan.ganai@icloud.com'
password = 'gxyj dswr aftp dbvn'


def sendMail(verbiage):
    # Create the message
    msg = MIMEMultipart('related')
    msg['Subject'] = 'ISRO has a new launch scheduled'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Create the HTML part with image CID reference
    html = f'''
    <html>
      <body>
        <h1>Hello!</h1>
        <p>ISRO has a new launch scheduled.</p>
        <p>{verbiage}</p>
        <img src="cid:myImage">
      </body>
    </html>
    '''

    # Attach HTML to the email
    msg.attach(MIMEText(html, 'html'))

    # Open image file and attach as MIMEImage
    with open('mission.png', 'rb') as img_file:
        img = MIMEImage(img_file.read())
        img.add_header('Content-ID', '<myImage>')
        img.add_header('Content-Disposition', 'inline', filename='mission.png')
        msg.attach(img)

    # Send email via SMTP
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
