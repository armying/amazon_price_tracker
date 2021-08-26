""" AUTOMATE AMAZON PRICE TRACKING, IF THE PRODUCT PRICE HITS THE DESIRED PRICE, SEND AN EMAIL TO SELF"""
from bs4 import BeautifulSoup
import requests
import smtplib

# Get the HTML of amazon website
URL = "https://www.amazon.com/Dell-S2721D-Ultra-Thin-DisplayPort-Certified/dp/B08G8SH4QJ/ref=sr_1_3?crid=3JSPYWW5VL" \
      "545&dchild=1&keywords=27%2Binch%2Bmonitor%2B1440p&qid=1618346518&sprefix=27%2Binch%2Bmonitor%2B14%2Caps%2C255&" \
      "sr=8-3&th=1"
HEADERS = {
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/89.0.4389.114 Safari/537.36",
}
DESIRED_PRICE = 240.00

response = requests.get(URL, headers=HEADERS)
web_html = response.text

# Create a BeautifulSoup object and scrape the price of the product
soup = BeautifulSoup(web_html, "html.parser")
price_tags = soup.find_all(name="span",
                           id="priceblock_ourprice",
                           class_="a-size-medium a-color-price priceBlockBuyingPriceString")
product_price = price_tags[0].getText()
product_price = float(product_price[1:])
print(f"The current price of the 27 inch Dell ultra-sharp monitor is: ${product_price}")

# Send an email if the product price hits the desired price
message = f"The current price of Dell S2721D 27 Inch 1440p QHD is ${product_price}, \n" \
          f"LINK: {URL}"
if product_price <= DESIRED_PRICE:
    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.starttls()
    sender_email = "YOUR EMAIL ADDRESS"
    g_app = "YOUR EMAIL's PASSWORD"
    try:
        connection.login(sender_email, g_app)
    except smtplib.SMTPAuthenticationError or smtplib.SMTPSenderRefused:
        print("Connection failed")
    connection.sendmail(sender_email, sender_email, msg=f"Subject: Dell S2721D 27 Inch 1440p QHD PRICE DROPPED!\n\n"
                                                        f"{message}")
    connection.quit()
