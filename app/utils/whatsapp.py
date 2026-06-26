import os
import requests

def send_whatsapp_book_notification(to_phone: str, book_title: str):
    """
    Dispatches a WhatsApp template message using Meta Cloud Graph API.
    """
     
    whatsapp_token = os.getenv("WHATSAPP_TOKEN")
    phone_number_id = os.getenv("PHONE_NUMBER_ID")

    if not whatsapp_token or not phone_number_id:
        print("⚠️ WhatsApp Notification skipped: Missing credentials in .env")
        return False

    
    url = f"https://graph.facebook.com/v25.0/{phone_number_id}/messages"
    
    headers = {
        "Authorization": f"Bearer {whatsapp_token}",
        "Content-Type": "application/json",
    }
    
     
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "template",
        "template": {
            "name": "jaspers_market_order_confirmation_v1",  # Pre-approved test template
            "language": {
                "code": "en_US"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": "Library System"}, 
                        {"type": "text", "text": book_title},        
                        {"type": "text", "text": "June 2026"}        
                    ]
                }
            ]
        }
    }

    try:
        # 4️⃣ Send the request to Meta's server infrastructure
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        response.raise_for_status()
        print(f"✅ WhatsApp alert successfully transmitted for book: {book_title}")
        return True
    except Exception as error:
        # Log the error but keep it non-blocking so it doesn't crash your FastAPI application
        print(f"❌ Failed to transmit WhatsApp dispatch: {error}")
        return False