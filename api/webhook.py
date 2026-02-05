from http.server import BaseHTTPRequestHandler
import json
import requests
import urllib.parse

TOKEN = "8512366652:AAHZIt4ZzHc2TtplWF61ljpSoM_is8lenbI" # သင့် Token ကို အမှန်ပြန်ထည့်ပါ

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"].get("text", "")

            if text == "/start":
                reply = "<b>🤖 QR & Link Generator Bot</b>\n\nစာသား သို့မဟုတ် Link တစ်ခုခု ပို့ပေးပါ။ ကျွန်တော်က QR ပုံရော၊ ပုံရဲ့ Link ကိုပါ ထုတ်ပေးပါ့မယ်။"
                payload = {"chat_id": chat_id, "text": reply, "parse_mode": "HTML"}
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json=payload)
            else:
                # 1. စာသားကို URL format ပြောင်းခြင်း
                encoded_text = urllib.parse.quote(text)
                
                # 2. QR Code Image Link တည်ဆောက်ခြင်း
                qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={encoded_text}"
                
                # 3. ပုံရော Link ပါတွဲပြီး ပို့ခြင်း
                caption_text = (
                    f"<b>✅ QR Code ထုတ်ပေးပြီးပါပြီ</b>\n\n"
                    f"<b>📝 မူရင်းစာသား:</b> <code>{text}</code>\n\n"
                    f"<b>🖼️ ပုံ Link:</b>\n{qr_url}"
                )
                
                photo_payload = {
                    "chat_id": chat_id,
                    "photo": qr_url,
                    "caption": caption_text,
                    "parse_mode": "HTML",
                    "reply_markup": {
                        "inline_keyboard": [
                            [
                                {"text": "🌐 ပုံကို Browser မှာကြည့်ရန်", "url": qr_url}
                            ]
                        ]
                    }
                }
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", json=photo_payload)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode())
