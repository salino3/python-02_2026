
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email_book_notification(
    destination_email: str, 
    recipient_name: str, 
    book_id: int, 
    book_title: str, 
    author_name: str
):
    """
    Establishes an encrypted SMTP tunnel to transmit a structured HTML/text 
    notification alerting users of fresh catalog additions.
    """
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT" )
    
    sender_email = os.getenv("SMTP_USERNAME") 
    password = os.getenv("SMTP_PASSWORD")
    
    # Make sure FRONT_PORT_DEV is handled or fallback to a default
    front_port_dev = os.getenv("FRONT_PORT_DEV")

    if not all([smtp_server, sender_email, password, destination_email]):
        print("⚠️ Email Notification skipped: Missing system credentials in .env")
        return False

    # 2. Build the message metadata envelope
    message = MIMEMultipart("alternative")
    message["Subject"] = f"📚 New Arrival: '{book_title}' has landed!"
    message["From"] = f"Next App Library <{sender_email}>"  
    message["To"] = f"{recipient_name} <{destination_email}>" 

    target_catalog_url = f"{front_port_dev}/books?search={book_id}"

    # 3. Personalize the text body with their name!
    text_body = (
        f"Hi {recipient_name},\n\n"
        f"A new book has arrived in Next App Library!\n\n"
        f"Book Name: {book_title}\n"
        f"By the Author: {author_name}\n\n"
        f"View details here: {target_catalog_url}"
    )

    # 4. Personalize the HTML body with their name
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; border: 1px solid #e0e0e0; padding: 20px; border-radius: 8px;">
          <h2 style="color: #4A90E2; margin-top: 0;">📚 New Library Arrival!</h2>
          <p>Hello <strong>{recipient_name}</strong>,</p>
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

    message.attach(MIMEText(text_body, "plain"))
    message.attach(MIMEText(html_body, "html"))

    try:
        server = smtplib.SMTP(smtp_server, int(smtp_port), timeout=5)
        server.starttls()  
        
     
        server.login(sender_email, password)
        
        server.sendmail(sender_email, destination_email, message.as_string())
        server.quit()
        
        print(f"📧 Email dispatch successfully sent to {recipient_name} ({destination_email}) for Book ID: {book_id}")
        return True
    except Exception as error:
        print(f"❌ Failed to transmit email notification to {recipient_name}: {error}")
        return False