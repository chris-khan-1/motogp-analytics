import json
from pathlib import Path

import requests
from playwright.sync_api import Request, sync_playwright

from app.enums.session import SessionType
from app.logger import LOGGER

MOTOGP_SESSION_CLASSIFICATION_PREFIX = (
    "https://api.pulselive.motogp.com/motogp/v2/results/classifications"
)


def get_motogp_classification_url(url: str) -> str:
    """
    Captures and returns the MotoGP classification API URL by intercepting network
    requests.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        classification_url: str | None = None

        def handle_classification_request(request: Request) -> None:
            nonlocal classification_url
            request_url = request.url
            if request_url.startswith(MOTOGP_SESSION_CLASSIFICATION_PREFIX):
                classification_url = request_url

        page.on(event="request", f=handle_classification_request)

        page.goto(url=url)

        page.wait_for_load_state(state="networkidle")

        context.close()
        browser.close()

    if classification_url is None:
        raise ValueError(f"Failed to capture classification URL for {url}")

    return classification_url


def format_race_data(data: dict) -> list[dict]:
    """Formats race and sprint session data into a structured list of dictionaries."""

    output = []
    for line in data["classification"]:
        position = line["position"]
        rider_full_name = line["rider"]["full_name"]
        average_speed = line["average_speed"]
        gap_to_first = line["gap"]["first"] if position else None
        total_time = line["time"]
        points = line["points"]
        total_laps = line["total_laps"]

        output.append(
            {
                "position": position,
                "rider": rider_full_name,
                "points": points,
                "average_speed": average_speed,
                "gap_to_first": gap_to_first,
                "total_time": total_time,
                "total_laps": total_laps,
            }
        )

    return output


def format_qualifying_data(data: dict) -> list[dict]:
    """Formats qualifying session data into a structured list of dictionaries."""

    output = []
    for line in data["classification"]:
        position = line["position"]
        rider_full_name = line["rider"]["full_name"]
        best_lap_time = line["best_lap"]["time"]
        gap_to_first = line["gap"]["first"] if position else None
        gap_to_previous = line["gap"]["prev"] if position else None
        total_laps = line["total_laps"]

        output.append(
            {
                "position": position,
                "rider": rider_full_name,
                "best_lap_time": best_lap_time,
                "gap_to_first": gap_to_first,
                "gap_to_previous": gap_to_previous,
                "total_laps": total_laps,
            }
        )

    return output


def write_session_data(
    data: list[dict], output_file_path: str
) -> None:  # pragma: no cover
    """Writes the session data to a JSON file after ensuring the directory exists."""

    Path(output_file_path).parent.mkdir(parents=True, exist_ok=True)

    with Path(output_file_path).open("w") as f:
        json.dump(data, f, indent=4)


def extract_and_write_session_data(
    year: str, event: str, session: str, round_number: str
) -> None:
    """Extracts session data for a given event and writes it to a JSON file."""

    base_url = "https://www.motogp.com/en/gp-results"
    full_url = f"{base_url}/{year}/{event}/motogp/{session}/classification"
    captured_url = get_motogp_classification_url(url=full_url)

    base_output_path = f"data/{year}/round_{round_number}"

    data = requests.get(url=captured_url, timeout=10).json()

    if session == SessionType.RACE.url_value:
        output_file_path = f"{base_output_path}/{SessionType.RACE}.json"
        formatted_data = format_race_data(data=data)
    elif session == SessionType.SPRINT.url_value:
        output_file_path = f"{base_output_path}/{SessionType.SPRINT}.json"
        formatted_data = format_race_data(data=data)
    elif session == SessionType.QUALIFYING_1.url_value:
        output_file_path = f"{base_output_path}/{SessionType.QUALIFYING_1}.json"
        formatted_data = format_qualifying_data(data=data)
    elif session == SessionType.QUALIFYING_2.url_value:
        output_file_path = f"{base_output_path}/{SessionType.QUALIFYING_2}.json"
        formatted_data = format_qualifying_data(data=data)
    else:
        raise ValueError(f"Session type '{session}' is not recognised.")

    write_session_data(data=formatted_data, output_file_path=output_file_path)
    LOGGER.info(f"Session data written to {output_file_path}")
