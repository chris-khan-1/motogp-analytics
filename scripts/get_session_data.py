import json
from pathlib import Path

from app.web_scraping.session_extraction import extract_and_write_session_data

year = "2025"

with Path(f"data/calendars/{year}_calendar.json").open() as f:
    calendar = json.load(f)

for event in calendar:
    extract_and_write_session_data(year=year, event=event["url_value"], session="rac")
