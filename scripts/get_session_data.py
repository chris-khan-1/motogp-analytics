import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from app.logger import LOGGER
from app.web_scraping.session_extraction import extract_and_write_session_data


def process_event(event: dict, year: str, session: str) -> None:
    return extract_and_write_session_data(
        year=year,
        event=event["url_value"],
        session=session,
        round_number=event["round"],
    )


if __name__ == "__main__":
    year = "2025"
    session = "rac"

    max_workers = 4

    with Path(f"data/{year}/{year}_calendar.json").open() as f:
        calendar = json.load(f)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_event, event, year, session) for event in calendar
        ]

        for future in as_completed(futures):
            try:
                result = future.result()
            except Exception as e:
                LOGGER.error(f"Error: {e}")
