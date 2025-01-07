from textwrap import dedent

import pytest

from app.web_scraping.pdf_extraction import (
    extract_classified_rider_race_results,
    split_classified_and_non_classified,
)


def test_split_classified_and_non_classified():
    input_text = dedent("""\
                Some
                Irrelevant
                Information
                Pos Pts # Rider Nation Team Motorcycle Total Time Km/h Gap
                1 25 93 Marc MARQUEZ SPA Ducati Lenovo Team DUCATI 40'04.628 169.8
                2 20 72 Marco BEZZECCHI ITA Aprilia Racing APRILIA 40'06.381 169.7 1.753
                Not classified
                23 Enea BASTIANINI ITA Red Bull KTM Tech3 KTM 11'33.792 168.2 15 laps
                More
                Irrelevant
                Information
                """)

    actual_classified, actual_non_classified = split_classified_and_non_classified(
        text=input_text
    )

    assert actual_classified == [
        "1 25 93 Marc MARQUEZ SPA Ducati Lenovo Team DUCATI 40'04.628 169.8",
        "2 20 72 Marco BEZZECCHI ITA Aprilia Racing APRILIA 40'06.381 169.7 1.753",
    ]
    assert actual_non_classified == [
        "23 Enea BASTIANINI ITA Red Bull KTM Tech3 KTM 11'33.792 168.2 15 laps"
    ]


@pytest.mark.parametrize(
    argnames=["input_info", "expected"],
    argvalues=[
        pytest.param(
            "1 25 93 Marc MARQUEZ SPA Ducati Lenovo Team DUCATI 40'04.628 169.8",
            {
                "position": 1,
                "points": 25,
                "rider_number": 93,
                "rider": "Marc MARQUEZ",
                "nation": "SPA",
                "team": "Ducati Lenovo Team",
                "bike": "DUCATI",
                "total_time": "40'04.628",
                "kmh": 169.8,
                "gap": None,
            },
            id="1st normal",
        ),
        pytest.param(
            "2 20 72 Marco BEZZECCHI ITA Aprilia Racing APRILIA 40'06.381 169.7 1.753",
            {
                "position": 2,
                "points": 20,
                "rider_number": 72,
                "rider": "Marco BEZZECCHI",
                "nation": "ITA",
                "team": "Aprilia Racing",
                "bike": "APRILIA",
                "total_time": "40'06.381",
                "kmh": 169.7,
                "gap": "1.753",
            },
            id="2nd normal",
        ),
        pytest.param(
            (
                "3 16 49 Fabio DI GIANNANTONIO ITA Pertamina Enduro VR46 Racing Team"
                " DUCATI 40'07.994 169.6 3.366"
            ),
            {
                "position": 3,
                "points": 16,
                "rider_number": 49,
                "rider": "Fabio DI GIANNANTONIO",
                "nation": "ITA",
                "team": "Pertamina Enduro VR46 Racing Team",
                "bike": "DUCATI",
                "total_time": "40'07.994",
                "kmh": 169.6,
                "gap": "3.366",
            },
            id="3rd multiple rider and team names",
        ),
    ],
)
def test_extract_classified_rider_race_results(input_info, expected):
    actual = extract_classified_rider_race_results(
        classified_rider_race_info=input_info
    )
    assert actual == expected
