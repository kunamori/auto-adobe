import requests as rq
from dotenv import load_dotenv
import os

# LOGIN URL VARIABLE
login_url = "https://software.kmutnb.ac.th/login/"
loggedin_url = "https://software.kmutnb.ac.th/download/"
adobe_url = "https://software.kmutnb.ac.th/adobe-reserve/processa.php"

# LOAD ENVIRONMENT VARIABLES
load_dotenv()

# GET USERNAME AND PASSWORD FROM ENVIRONMENT VARIABLES
username = os.getenv("KMUTNB_USERNAME")
password = os.getenv("KMUTNB_PASSWORD")

# HEADERS PAYLOAD
payload_headers = {
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": "\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Upgrade-Insecure-Requests": "1",
        "Origin": "https://software.kmutnb.ac.th",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/135.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://software.kmutnb.ac.th/login/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "th-TH,th;q=0.9",
        "Connection": "close"
}

# DATA PAYLOAD
payload_data = {
        "myusername": username,
        "mypassword": password,
        "Submit": ''
}

# HEADER AND DATA (Adobe Process)
adobe_url = "https://software.kmutnb.ac.th:443/adobe-reserve/add2.php"
adobe_headers = {
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": "\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Upgrade-Insecure-Requests": "1",
        "Origin": "https://software.kmutnb.ac.th",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/135.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://software.kmutnb.ac.th/adobe-reserve/processa.php",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "th-TH,th;q=0.9",
        "Connection": "close"
}

adobe_data = {
        "userId": '',
        "date_expire": "2024-09-01",
        "status_number": "0",
        "Submit_get": ''
}

# USING SESSION FOR HOLD SESSION FOR GRANT ADOBE ACCESS
with rq.session() as rqss:
        rqss.post(login_url, headers=payload_headers, data=payload_data, verify=False)
        req3 = rqss.post(adobe_url, headers=adobe_headers, data=adobe_data, verify=False)
        print(req3.text)
