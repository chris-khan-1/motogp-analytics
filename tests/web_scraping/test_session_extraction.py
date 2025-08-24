from unittest import mock
from unittest.mock import Mock, patch

import pytest

from app.web_scraping.session_extraction import (
    MOTOGP_SESSION_CLASSIFICATION_PREFIX,
    extract_and_write_session_data,
    format_qualifying_data,
    format_race_data,
    get_motogp_classification_url,
)

_PATCH_BASE_PATH = "app.web_scraping.session_extraction"


@pytest.mark.integration
@pytest.mark.parametrize(
    argnames="input_url",
    argvalues=[
        "https://www.motogp.com/en/gp-results/2025/qat/moto2/q2/classification",
        "https://www.motogp.com/en/gp-results/2025/tha/moto3/fp1/classification",
        "https://www.motogp.com/en/gp-results/2025/por/motogp/q1/classification",
    ],
)
def test_get_motogp_classification_url_different_races(input_url):
    """Test that the function works with different race configurations"""
    actual = get_motogp_classification_url(url=input_url)

    assert actual.startswith(MOTOGP_SESSION_CLASSIFICATION_PREFIX)
    assert "?session=" in actual


@pytest.mark.integration
def test_get_motogp_classification_url_invalid_url():
    bad_url = "https://www.example.com"

    with pytest.raises(
        ValueError,
        match=f"Failed to capture classification URL for {bad_url}",
    ):
        get_motogp_classification_url(url=bad_url)


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


def test_format_qualifying_data():
    input_data = {
        "classification": [
            {
                "position": 1,
                "rider": {
                    "full_name": "Maverick Vi\u00f1ales",
                },
                "best_lap": {"number": 6, "time": "01:36.284"},
                "total_laps": 6,
                "gap": {"first": "0.000", "prev": "0.000"},
            },
            {
                "position": 2,
                "rider": {
                    "full_name": "Marco Bezzecchi",
                },
                "best_lap": {"number": 7, "time": "01:36.451"},
                "total_laps": 9,
                "gap": {"first": "0.167", "prev": "0.167"},
            },
            {
                "position": 3,
                "rider": {
                    "full_name": "Brad Binder",
                },
                "best_lap": {"number": 6, "time": "01:36.584"},
                "total_laps": 8,
                "gap": {"first": "0.300", "prev": "0.133"},
            },
        ]
    }

    expected = [
        {
            "position": 1,
            "rider": "Maverick Vi\u00f1ales",
            "best_lap_time": "01:36.284",
            "gap_to_first": "0.000",
            "gap_to_previous": "0.000",
            "total_laps": 6,
        },
        {
            "position": 2,
            "rider": "Marco Bezzecchi",
            "best_lap_time": "01:36.451",
            "gap_to_first": "0.167",
            "gap_to_previous": "0.167",
            "total_laps": 9,
        },
        {
            "position": 3,
            "rider": "Brad Binder",
            "best_lap_time": "01:36.584",
            "gap_to_first": "0.300",
            "gap_to_previous": "0.133",
            "total_laps": 8,
        },
    ]

    actual = format_qualifying_data(data=input_data)

    assert actual == expected


@pytest.mark.parametrize(
    argnames=("input_session", "session_full_name"),
    argvalues=[
        pytest.param("rac", "race", id="race session"),
        pytest.param("spr", "sprint", id="sprint session"),
    ],
)
@patch(f"{_PATCH_BASE_PATH}.get_motogp_classification_url")
@patch(f"{_PATCH_BASE_PATH}.requests.get")
@patch(f"{_PATCH_BASE_PATH}.format_race_data")
@patch(f"{_PATCH_BASE_PATH}.write_session_data")
def test_extract_and_write_session_data_race_or_sprint(
    mock_write_session_data,
    mock_format_race_data,
    mock_requests_get,
    mock_get_motogp_classification_url,
    input_session,
    session_full_name,
):
    mock_get_motogp_classification_url.return_value = "The classidication URL"

    extract_and_write_session_data(
        year="2025", event="spa", session=input_session, round_number="4"
    )

    mock_get_motogp_classification_url.assert_called_once_with(
        url=(
            f"https://www.motogp.com/en/gp-results/2025/spa/motogp/{input_session}"
            "/classification"
        )
    )

    mock_requests_get.assert_called_once_with(url="The classidication URL", timeout=10)

    mock_format_race_data.assert_called_once()
    mock_write_session_data.assert_called_once_with(
        data=mock.ANY, output_file_path=f"data/2025/round_4/{session_full_name}.json"
    )


@pytest.mark.parametrize(
    argnames=("input_session", "session_full_name"),
    argvalues=[
        pytest.param("q1", "q1", id="q1 session"),
        pytest.param("q2", "q2", id="q2 session"),
    ],
)
@patch(f"{_PATCH_BASE_PATH}.get_motogp_classification_url")
@patch(f"{_PATCH_BASE_PATH}.requests.get")
@patch(f"{_PATCH_BASE_PATH}.format_qualifying_data")
@patch(f"{_PATCH_BASE_PATH}.write_session_data")
def test_extract_and_write_session_data_q1_or_q2(
    mock_write_session_data,
    mock_format_qualifying_data,
    mock_requests_get,
    mock_get_motogp_classification_url,
    input_session,
    session_full_name,
):
    mock_get_motogp_classification_url.return_value = "The classidication URL"

    extract_and_write_session_data(
        year="2025", event="spa", session=input_session, round_number="4"
    )

    mock_get_motogp_classification_url.assert_called_once_with(
        url=(
            f"https://www.motogp.com/en/gp-results/2025/spa/motogp/{input_session}"
            "/classification"
        )
    )

    mock_requests_get.assert_called_once_with(url="The classidication URL", timeout=10)

    mock_format_qualifying_data.assert_called_once()
    mock_write_session_data.assert_called_once_with(
        data=mock.ANY, output_file_path=f"data/2025/round_4/{session_full_name}.json"
    )


@patch(f"{_PATCH_BASE_PATH}.get_motogp_classification_url", Mock())
@patch(f"{_PATCH_BASE_PATH}.requests.get", Mock())
def test_extract_and_write_session_data_invalid_session():
    with pytest.raises(
        ValueError, match="Session type 'INVALID SESSION' is not recognised."
    ):
        extract_and_write_session_data(
            year="2025", event="spa", session="INVALID SESSION", round_number="4"
        )
