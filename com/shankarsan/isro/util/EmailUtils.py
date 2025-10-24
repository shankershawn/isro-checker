import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from loggers.NoDuplicateLogger import no_duplicate_logger


def sendMail(verbiage, subject, from_addr, from_pass, to_addr):
    # Create the message
    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr

    # Create the HTML part with image CID reference
    html = f'''
    <html>
      <body>
        <h1>Hello!</h1>
        <p>ISRO has a new launch scheduled.</p>
        <p>{verbiage}</p>
        <img src="cid:myImage">
        <p>Click <a href="https://lvg.shar.gov.in/VSCREGISTRATION/index.jsp">here</a> to register.</p>
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
        server.login(from_addr, from_pass)
        server.sendmail(from_addr, to_addr, msg.as_string())
        no_duplicate_logger.info(f"Email sent to {to_addr} regarding ISRO mission update.")
