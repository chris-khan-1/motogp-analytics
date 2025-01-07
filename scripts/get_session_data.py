import json
from pathlib import Path

import requests

from app.web_scraping.session_extraction import get_motogp_classification_url

if __name__ == "__main__":
    captured_url = get_motogp_classification_url(
        url="https://www.motogp.com/en/gp-results/2025/gbr/motogp/rac/classification"
    )

    result = requests.get(url=captured_url, timeout=10)

    with Path.open("tests/test_data/example_raw_race_output.json", "w") as f:
        json.dump(result.json(), f, indent=4)
