from unittest.mock import patch

import pytest

from app.web_scraping.session_extraction import (
    MOTOGP_SESSION_CLASSIFICATION_PREFIX,
    extract_and_write_session_data,
    format_race_data,
    get_motogp_classification_url,
)

_PATCH_BASE_PATH = "app.web_scraping.session_extraction"


@pytest.mark.integration
@pytest.mark.parametrize(
    argnames="test_url",
    argvalues=[
        "https://www.motogp.com/en/gp-results/2025/qat/moto2/q2/classification",
        "https://www.motogp.com/en/gp-results/2025/tha/moto3/fp1/classification",
        "https://www.motogp.com/en/gp-results/2025/por/motogp/q1/classification",
    ],
)
def test_get_motogp_classification_url_different_races(test_url):
    """Test that the function works with different race configurations"""
    actual = get_motogp_classification_url(url=test_url)

    assert actual.startswith(MOTOGP_SESSION_CLASSIFICATION_PREFIX)
    assert "?session=" in actual


def test_format_race_data():
    input_data = {
        "classification": [
            {
                "position": 1,
                "rider": {
                    "full_name": "Marco Bezzecchi",
                },
                "average_speed": 175.7,
                "gap": {"first": "0.000", "lap": "0"},
                "total_laps": 19,
                "time": "38:16.037",
                "points": 25,
            },
            {
                "position": None,
                "rider": {
                    "full_name": "Aleix Espargaro",
                },
                "average_speed": 163.3,
                "gap": {"first": "0.000", "lap": "16"},
                "total_laps": 3,
                "time": "06:30.109",
                "points": 0,
            },
        ]
    }

    expected = [
        {
            "position": 1,
            "rider": "Marco Bezzecchi",
            "points": 25,
            "average_speed": 175.7,
            "gap_to_first": "0.000",
            "total_time": "38:16.037",
            "total_laps": 19,
        },
        {
            "position": None,
            "rider": "Aleix Espargaro",
            "average_speed": 163.3,
            "points": 0,
            "gap_to_first": None,
            "total_time": "06:30.109",
            "total_laps": 3,
        },
    ]

    actual = format_race_data(data=input_data)

    assert actual == expected


@patch(f"{_PATCH_BASE_PATH}.get_motogp_classification_url")
@patch(f"{_PATCH_BASE_PATH}.requests.get")
@patch(f"{_PATCH_BASE_PATH}.format_race_data")
@patch(f"{_PATCH_BASE_PATH}.write_session_data")
def test_main_with_race_session(
    mock_write_session_data,
    mock_format_race_data,
    mock_requests_get,
    mock_get_motogp_classification_url,
):
    mock_get_motogp_classification_url.return_value = "The classidication URL"
    extract_and_write_session_data(year="2025", event="spa", session="rac")

    mock_get_motogp_classification_url.assert_called_once_with(
        url="https://www.motogp.com/en/gp-results/2025/spa/motogp/rac/classification"
    )

    mock_requests_get.assert_called_once_with(url="The classidication URL", timeout=10)

    mock_format_race_data.assert_called_once()
    mock_write_session_data.assert_called_once()
