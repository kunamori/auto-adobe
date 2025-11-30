"""
payload.py

Script to automate login and Adobe reservation actions on the KMUTNB software portal.

Purpose
- Log in to https://software.kmutnb.ac.th using credentials provided via environment
  variables.
- Submit a request to the portal's Adobe reservation endpoint to extend/grant access
  (the script computes a target `date_expire` value automatically).

Usage
- Provide credentials via environment variables:
    - KMUTNB_USERNAME
    - KMUTNB_PASSWORD
- The script uses a requests.Session to maintain cookies between the login step and
  the Adobe reservation POST.
- This module is intended to be executed as a small automation helper; it is not a
  reusable library API.

Security and operational notes
- Credentials are read from environment variables; avoid committing them to source.
- The script currently disables SSL verification in requests (`verify=False`) to
  match the original behavior. In production, enable verification or provide a
  proper CA bundle.
- HTTP responses are minimally validated; you may want to add more robust error
  handling, logging, retries, and timeouts depending on your needs.

Linting
- Module-level constants are UPPER_CASE to satisfy common linting rules.
- Standard library imports come before third-party imports.
"""

import os
from datetime import date as _date

import requests as rq
from dotenv import load_dotenv

# LOGIN/ENDPOINT URL CONSTANTS
LOGIN_URL = "https://software.kmutnb.ac.th/login/"
LOGGEDIN_URL = "https://software.kmutnb.ac.th/download/"
ADOBE_PROCESS_URL = "https://software.kmutnb.ac.th/adobe-reserve/processa.php"
ADOBE_URL = "https://software.kmutnb.ac.th:443/adobe-reserve/add2.php"

# Load environment variables from a .env file (if present) and the environment
load_dotenv()

# Credentials from environment
username = os.getenv("KMUTNB_USERNAME")
password = os.getenv("KMUTNB_PASSWORD")

# Headers used for the login POST
payload_headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:146.0) Gecko/20100101 Firefox/146.0",
    "Origin": "https://software.kmutnb.ac.th",
    "Referer": LOGIN_URL,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# Login form data
payload_data = {"myusername": username, "mypassword": password, "Submit": ""}


def make_date_expire(dt: _date) -> str:
    """
    Compute the first day of the next month using the original script's logic.

    The original one-liner used a special case where if month == 1, the year was
    decremented by 1 and the month set to 12; this function preserves that behavior.
    Returns a string formatted as 'YYYY-MM-01'.
    """
    if dt.month == 1:
        year = dt.year - 1
        month = 12
    else:
        year = dt.year
        month = dt.month + 1
    return f"{year:04d}-{month:02d}-01"


# Adobe process headers and data
adobe_headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:146.0) Gecko/20100101 Firefox/146.0",
    "Origin": "https://software.kmutnb.ac.th",
    "Referer": ADOBE_PROCESS_URL,
}

adobe_data = {
    "userId": "",
    "date_expire": make_date_expire(_date.today()),
    "status_number": "0",
    "Submit_get": "",
}


def main():
    """Run the login + Adobe reservation sequence."""
    # Using a session preserves cookies between requests
    with rq.session() as session:
        # Perform login. Capture and check the response so failures are visible.
        login_resp = session.post(
            LOGIN_URL,
            headers=payload_headers,
            data=payload_data,
            verify=False,
            timeout=10,
        )
        try:
            login_resp.raise_for_status()
        except rq.RequestException:
            # If login fails, propagate the exception after printing minimal info.
            print(
                "Login request failed with status:",
                getattr(login_resp, "status_code", None),
            )
            raise

        # Submit Adobe reservation/add request
        req3 = session.post(
            ADOBE_URL, headers=adobe_headers, data=adobe_data, verify=False, timeout=10
        )
        # Print the response body for visibility (original behavior)
        print(req3.text)


if __name__ == "__main__":
    main()
