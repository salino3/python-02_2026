import os
import requests
 

def send_whatsapp_book_notification(to_phone: str, book_title: str, author_name: str):
    """
    An absolute raw replica of the working Meta curl payload.
    """
    whatsapp_token = os.getenv("WHATSAPP_TOKEN")
    phone_number_id = os.getenv("PHONE_NUMBER_ID")

    if not whatsapp_token or not phone_number_id:
        print("⚠️ WhatsApp Notification skipped: Missing credentials in .env")
        return False

    # Debug line: Let's see exactly what token python is loading
    print(f"DEBUG: Using Token starting with: {whatsapp_token[:15]}...")
    print(f"DEBUG: Using Phone ID: {phone_number_id}")

    url = f"https://graph.facebook.com/v25.0/{phone_number_id}/messages"
    
    headers = {
        "Authorization": f"Bearer {whatsapp_token.strip()}", # .strip() removes accidental spaces
        "Content-Type": "application/json",
    }
    
    # 🌟 BYTE-FOR-BYTE EXACT DUPLICATE OF YOUR WEB CURL JSON PAYLOAD
    payload = {
        "messaging_product": "whatsapp",
        "to": str(to_phone).strip(),
        "type": "template",
        "template": { 
            "name": "jaspers_market_order_confirmation_v1",
            "language": { 
                "code": "en_US" 
            },
            "components": [
                { 
                    "type": "body", 
                    "parameters": [
                        { "type": "text", "text": "Next App Library" }, 
                        { "type": "text", "text": book_title }, 
                        { "type": "text", "text": f"By {author_name} - http://localhost:3600/books" }
                    ] 
                }
            ] 
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        response.raise_for_status()
        print(f"✅ WhatsApp alert successfully transmitted!")
        return True
    except Exception as error:
        # If it fails, print the full error response body from Meta's server
        if hasattr(error, 'response') and error.response is not None:
            print(f"❌ Meta API Error Response: {error.response.text}")
        else:
            print(f"❌ Failed to transmit WhatsApp dispatch: {error}")
        return False