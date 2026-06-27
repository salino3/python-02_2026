# app/utils/email_service.py
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

FRONT_PORT_DEV = os.getenv("FRONT_PORT_DEV")

def send_email_book_notification(book_id: int, book_title: str, author_name: str):
    """
    Establishes an encrypted SMTP tunnel to transmit a structured HTML/text 
    notification alerting users of fresh catalog additions.
    """
    
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT", "587")
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    receiver = os.getenv("RECEIVER_EMAIL")

    if not all([smtp_server, username, password, receiver]):
        print("⚠️ Email Notification skipped: Missing credentials in .env")
        return False

   
    message = MIMEMultipart("alternative")
    message["Subject"] = f"📚 New Arrival: '{book_title}' has landed!"
    message["From"] = username
    message["To"] = receiver

    target_catalog_url = f"{FRONT_PORT_DEV}/books?search={book_id}"

    text_body = (
        f"A new book has arrived in Next App Library!\n\n"
        f"Book Name: {book_title}\n"
        f"By the Author: {author_name}\n\n"
        f"View details here: {target_catalog_url}"
    )

    # HTML body for rich rendering inside user mail applications
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; border: 1px solid #e0e0e0; padding: 20px; border-radius: 8px;">
          <h2 style="color: #4A90E2; margin-top: 0;">📚 New Library Arrival!</h2>
          <p>A brand new title has just been cataloged into the system:</p>
          <blockquote style="background: #f9f9f9; border-left: 5px solid #4A90E2; padding: 10px 15px; margin: 15px 0;">
            <strong>📖 Title:</strong> {book_title}<br>
            <strong>✍️ Author:</strong> {author_name}
          </blockquote>
          <div style="margin-top: 25px;">
            <a href="{target_catalog_url}" style="background-color: #4A90E2; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">
              View Catalog Record
            </a>
          </div>
        </div>
      </body>
    </html>
    """

    # Attach both alternative parts to the mail container object
    message.attach(MIMEText(text_body, "plain"))
    message.attach(MIMEText(html_body, "html"))

    try:
        server = smtplib.SMTP(smtp_server, int(smtp_port), timeout=5)
        server.starttls()  # Upgrades the plain text connection to an encrypted secure SSL layer
        server.login(username, password)
        server.sendmail(username, receiver, message.as_string())
        server.quit()
        
        print(f"📧 Email dispatch successfully sent for Book ID: {book_id}")
        return True
    except Exception as error:
        print(f"❌ Failed to transmit email notification: {error}")
        return False