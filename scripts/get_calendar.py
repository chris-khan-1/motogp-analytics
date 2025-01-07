"""Writes the calendar data for a given year to a JSON file."""

import json
import logging
from pathlib import Path

from app.web_scraping.event_extraction import get_event_data_for_year

years = map(str, range(2025, 2026))

for year in years:
    events_data = get_event_data_for_year(year=year)

    output_file_path = f"data/calendars/calendar_{year}.json"

    with Path(output_file_path).open("w") as json_file:
        json.dump(events_data, json_file, indent=4)

    logging.info(f"Calendar data for {year} has been written to {output_file_path}")
