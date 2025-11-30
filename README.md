# Auto-Adobe

Automate your sign-in to the KMUTNB Software Center and trigger an Adobe license reservation in one shot.

This repository contains a minimal Python script that:
- Loads your credentials from environment variables.
- Logs in to `https://software.kmutnb.ac.th/login/`.

Intended audience: students and staff who already have legitimate access and permissions granted by KMUTNB. Use responsibly and in accordance with the university policies and the website's terms of service.

> [!CAUTION]
> ## Legal and ethical notice
>
> This script is provided for personal convenience where automation is permitted. You are responsible for complying with KMUTNB policies and all applicable terms of service. Do not use this script to circumvent security, access controls, or usage limits.

## How it works

High-level flow:
1. Load `USERNAME` and `PASSWORD` from a local `.env` file using `python-dotenv`.
2. Create a `requests.Session` to persist cookies between requests.
3. POST credentials to the login endpoint.
4. POST to the Adobe reservation endpoint (`/adobe-reserve/add2.php`) with required payload.
5. Print the raw response (HTML) from the Adobe endpoint so you can verify success.

## Prerequisites

- Python 3.9+ recommended.
- A valid KMUTNB account with access to Adobe reservation.
- Network access to `software.kmutnb.ac.th`.

## Setup

1. Create and activate a virtual environment (recommended):
   - Windows (PowerShell): run `python -m venv .venv` then `.venv\Scripts\Activate.ps1`
   - macOS/Linux (bash/zsh): run `python3 -m venv .venv` then `source .venv/bin/activate`

2. Install dependencies:
   - `pip install -r requirements.txt`

3. Create a `.env` file in the project root with the following contents:
   - `USERNAME=your_username`
   - `PASSWORD=your_password`

   Notes:
   - The `.env` file is ignored by version control. Do not commit secrets.
   - You can also export environment variables instead of using `.env`.

## Usage

- From the project root, run:
  - Windows: `python src/payload.py` (or use `.venv\Scripts\python.exe src\payload.py` if using a venv)
  - macOS/Linux: `python3 src/payload.py`

What to expect:
- The script prints the raw HTML returned by the Adobe reservation endpoint. Look for cues like a success message or confirmation text specific to the site. If the site’s response changes over time, you may need to adjust how you detect success.

## Scheduling (optional)

You can run the script on a schedule to keep your reservation active or to automatically request access at specific times. Be sure this aligns with site policies.

- Windows Task Scheduler:
  1. Open Task Scheduler and create a new Basic Task.
  2. Set a trigger (daily/weekly).
  3. Action: Start a program.
  4. Program/script: full path to your Python interpreter (e.g., `C:\path\to\Auto-Adobe\.venv\Scripts\python.exe`).
  5. Add arguments: `src\payload.py`
  6. Start in: the project directory (e.g., `C:\path\to\Auto-Adobe`)
  7. Ensure the `.env` file is present in the working directory or use system environment variables.

- Linux/macOS cron:
  1. Activate your venv or reference it explicitly in your cron line.
  2. Add a cron entry such as:
     - `0 8 * * 1-5 /path/to/Auto-Adobe/.venv/bin/python /path/to/Auto-Adobe/src/payload.py`
  3. Ensure environment variables are available to cron (either set globally or use a wrapper script that sources them).

- systemd timer (Linux):
  - Create a service that runs your venv’s Python with `src/payload.py`, and pair it with a `.timer` unit. Make sure the service `WorkingDirectory` is the repository root so the `.env` loads.

## Troubleshooting

- Login fails (401/403 or redirected back to login):
  - Verify `USERNAME` and `PASSWORD` are correct.
  - The site may require additional tokens (CSRF) or a prior GET to establish cookies. You may need to:
    - Perform a GET to the login page and parse hidden inputs.
    - Carry those tokens into the POST request.
  - The site may have introduced CAPTCHA or other bot protection, which will block automation.

## Security best practices

- Never commit `.env` or credentials. The `.gitignore` in this project already ignores `.env`.
- Rotate your password periodically and immediately if you suspect compromise.
- Use a separate, least-privilege account for automation if possible.
- When scheduling, ensure the account running the task has access to the `.env` securely and that logs do not dump secrets.
- Prefer enabling SSL verification to mitigate MITM risks.
