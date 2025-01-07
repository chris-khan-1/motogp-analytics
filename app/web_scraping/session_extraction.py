import json
import logging
from pathlib import Path

import requests
from playwright.sync_api import Request, sync_playwright

MOTOGP_SESSION_CLASSIFICATION_PREFIX = (
    "https://api.pulselive.motogp.com/motogp/v2/results/classifications"
)


def get_motogp_classification_url(url: str) -> str | None:
    """
    Captures and returns the MotoGP classification API URL by intercepting network
    requests.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        classification_url = None

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
        return classification_url


def format_race_data(data: list[dict]) -> list[dict]:
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


def write_session_data(
    data: list[dict], output_file_name: str
) -> None:  # pragma: no cover
    with Path.open(output_file_name, "w") as f:
        json.dump(data, f, indent=4)


def main(year: str, event: str, session: str) -> None:
    base_url = "https://www.motogp.com/en/gp-results"
    full_url = f"{base_url}/{year}/{event}/motogp/{session}/classification"
    captured_url = get_motogp_classification_url(url=full_url)

    if captured_url:
        data = requests.get(url=captured_url, timeout=10).json()
    else:
        logging.error("Failed to capture classification URL.")

    output_file_path = f"data/results/{year}/{event}/{session}.json"

    Path(output_file_path).parent.mkdir(parents=True, exist_ok=True)

    if session == "rac":
        formatted_data = format_race_data(data=data)
    else:
        logging.warning(f"Session type '{session}' is not handled. No output written.")

    write_session_data(data=formatted_data, output_file_name=output_file_path)
