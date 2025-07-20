from app.utils.pdf_extraction import (
    extract_results,
    parse_classified,
    parse_non_classified,
)


def test_parse_classified_basic():
    parts = [
        "1",
        "25",
        "93",
        "Marc",
        "MARQUEZ",
        "SPA",
        "Ducati",
        "Lenovo",
        "Team",
        "DUCATI",
        "40'04.628",
        "169.8",
    ]
    # Insert team and bike in correct positions
    parts = [
        "1",
        "25",
        "93",
        "Marc",
        "MARQUEZ",
        "SPA",
        "Ducati",
        "Lenovo",
        "Team",
        "DUCATI",
        "40'04.628",
        "169.8",
    ]
    result = parse_classified(parts)
    assert result["position"] == 1
    assert result["points"] == 25
    assert result["number"] == 93
    assert result["rider"] == "Marc MARQUEZ"
    assert result["nation"] == "SPA"
    assert result["team"] == "Ducati Lenovo Team"
    assert result["bike"] == "DUCATI"
    assert result["total_time"] == "40'04.628"
    assert result["kmh"] == 169.8
    assert result["gap"] is None


def test_parse_classified_no_points():
    parts = [
        "16",
        "49",
        "Fabio",
        "DI",
        "GIANNANTONIO",
        "ITA",
        "Pertamina",
        "Enduro",
        "VR46",
        "Racing",
        "Team",
        "DUCATI",
        "40'29.357",
        "168.1",
        "24.729",
    ]
    result = parse_classified(parts)
    assert result["position"] == 16
    assert result["points"] == 49
    assert result["number"] is None


def test_parse_non_classified_basic():
    parts = [
        "21",
        "Alex",
        "MARQUEZ",
        "SPA",
        "Gresini",
        "Racing",
        "MotoGP",
        "DUCATI",
        "40'35.000",
        "167.5",
        "31.000",
    ]
    result = parse_non_classified(parts)
    assert result["position"] is None
    assert result["points"] is None
    assert result["number"] == 21
    assert result["rider"] == "Alex MARQUEZ"
    assert result["nation"] == "SPA"
    assert "Gresini Racing MotoGP" in result["team"]
    assert result["bike"] == "DUCATI"
    assert result["total_time"] == "40'35.000"
    assert result["kmh"] == 167.5
    assert result["gap"] == "31.000"


def test_extract_results_mixed():
    text = (
        "Pos Pts # Rider Nation Team Motorcycle Total Time Km/h Gap\n"
        "1 25 93 Marc MARQUEZ SPA Ducati Lenovo Team DUCATI 40'04.628 169.8\n"
        "Not classified\n"
        "21 Alex MARQUEZ SPA Gresini Racing MotoGP DUCATI 40'35.000 167.5 31.000\n"
    )
    results = extract_results(text)
    assert len(results) == 2
    assert results[0]["position"] == 1
    assert results[1]["position"] is None
    assert results[1]["rider"] == "Alex MARQUEZ"
