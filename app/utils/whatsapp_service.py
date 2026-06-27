import os
import requests
 
FRONT_PORT_DEV = os.getenv("FRONT_PORT_DEV")

def send_whatsapp_book_notification(to_phone: str, book_id: int, book_title: str, author_name: str):
    """
    Dispatches a structured notification using the working Meta template blueprint.
    """
    whatsapp_token = os.getenv("WHATSAPP_TOKEN")
    phone_number_id = os.getenv("PHONE_NUMBER_ID")

    if not whatsapp_token or not phone_number_id:
        print("⚠️ WhatsApp Notification skipped: Missing credentials in .env")
        return False

    url = f"https://graph.facebook.com/v25.0/{phone_number_id}/messages"
    
    headers = {
        "Authorization": f"Bearer {whatsapp_token.strip()}",
        "Content-Type": "application/json",
    }
    
    target_catalog_url = f"{FRONT_PORT_DEV}/books?search={book_id}"
 
 
    clean_message_text = (
        f"A new book has arrived in Next App Library!\n\n"
        f"📖 Book Name: '{book_title}'\n"
        f"✍️ By the Author: '{author_name}'\n\n"
        f"🔗 View details at: {target_catalog_url}"
    )

    
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": str(to_phone).strip(),
        "type": "text",
        "text": {
            "preview_url": True,  
            "body": clean_message_text
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        response.raise_for_status()
        print(f"✅ WhatsApp dynamic entry alert dispatched for Book ID: {book_id}")
        return True
    except Exception as error:
        if hasattr(error, 'response') and error.response is not None:
            print(f"❌ Meta API Error Response: {error.response.text}")
        else:
            print(f"❌ Failed to transmit WhatsApp dispatch: {error}")
        return False