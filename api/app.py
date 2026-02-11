from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread
import time
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

app = Flask(__name__)
CORS(app)

# Function to send email alerts
def send_email_alert(email_receiver, subject, message):
    EMAIL_SENDER =os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD =os.getenv("EMAIL_PASSWORD")

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = email_receiver

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, email_receiver, msg.as_string())
        print(f"Email Sent: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to get the price from the given URL
def get_price(url, selector,retries=3):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(3)
        price_text = driver.find_element(By.CSS_SELECTOR, selector).text
        driver.quit()
        return float(price_text.replace("₹", "").replace(",", "").strip())
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

# Background price checker function
def price_checker(data):
    amazon_url = data["amazon_url"]
    flipkart_url = data["flipkart_url"]
    email_receiver = data["email"]
    target_price = float(data["target_price"])

    send_email_alert(email_receiver, "✅ Price Alert Service Started!", f"Tracking prices...{target_price}is seted sucessfully.")

    while True:
        print("Checking prices...")
        amazon_price = get_price(amazon_url, ".a-price-whole") if amazon_url else None
        flipkart_price = get_price(flipkart_url, "._30jeq3._16Jk6d") if flipkart_url else None

        if amazon_price and amazon_price <= target_price:
            send_email_alert(email_receiver, "🔥 Amazon Price Drop Alert!", f"Price: ₹{amazon_price}\n{amazon_url}")

        if flipkart_price and flipkart_price <= target_price:
            send_email_alert(email_receiver, "🔥 Flipkart Price Drop Alert!", f"Price: ₹{flipkart_price}\n{flipkart_url}")

        print("Sleeping for 1 hour...")
        time.sleep(3600)

# Route to accept data from frontend
@app.route("/start-tracking", methods=["POST"])
def start_tracking():
    data = request.json
    Thread(target=price_checker, args=(data,), daemon=True).start()
    return jsonify({"status": "Tracking started"}), 200

# Home route
@app.route("/")
def home():
    return jsonify({"status": "Price Alert Service is running!"})

if __name__ == "__main__":
    app.run(debug=True,port=5000)