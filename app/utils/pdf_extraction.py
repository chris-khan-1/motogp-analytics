import io
import json
import re
from pathlib import Path

import pdfplumber
import requests


def parse_classified(parts: list[str]) -> dict[str, str | int | float | None]:
    try:
        position = int(parts[0])
    except ValueError:
        return None
    try:
        points = int(parts[1])
        number = int(parts[2])
        idx_number = 2
    except ValueError:
        points = None
        number = int(parts[1])
        idx_number = 1

    nation_idx = next(
        (
            i
            for i in range(idx_number + 1, len(parts))
            if re.fullmatch(r"[A-Z]{3}", parts[i])
        ),
        None,
    )
    if nation_idx is None:
        return None
    rider = " ".join(parts[idx_number + 1 : nation_idx])
    nation = parts[nation_idx]

    bike_idx = next(
        (
            i
            for i in range(len(parts) - 4, nation_idx, -1)
            if re.fullmatch(r"[A-Z]+", parts[i])
        ),
        None,
    )
    if bike_idx is None:
        return None
    team = " ".join(parts[nation_idx + 1 : bike_idx])
    bike = parts[bike_idx]
    total_time = parts[bike_idx + 1]
    try:
        kmh = float(parts[bike_idx + 2])
    except ValueError:
        kmh = None
    gap = " ".join(parts[bike_idx + 3 :]) if len(parts) > bike_idx + 3 else None

    return {
        "position": position,
        "points": points,
        "number": number,
        "rider": rider,
        "nation": nation,
        "team": team,
        "bike": bike,
        "total_time": total_time,
        "kmh": kmh,
        "gap": gap if gap else None,
    }


def parse_non_classified(parts: list) -> dict:
    try:
        number = int(parts[0])
    except ValueError:
        return None
    nation_idx = next(
        (i for i in range(1, len(parts)) if re.fullmatch(r"[A-Z]{3}", parts[i])),
        None,
    )
    if nation_idx is None:
        return None
    rider = " ".join(parts[1:nation_idx])
    nation = parts[nation_idx]
    bike_idx = next(
        (
            i
            for i in range(nation_idx + 1, len(parts))
            if re.fullmatch(r"[A-Z]+", parts[i])
        ),
        None,
    )
    if bike_idx is None:
        return None
    team = " ".join(parts[nation_idx + 1 : bike_idx])
    bike = parts[bike_idx]
    total_time = parts[bike_idx + 1] if len(parts) > bike_idx + 1 else None
    try:
        kmh = float(parts[bike_idx + 2]) if len(parts) > bike_idx + 2 else None
    except ValueError:
        kmh = None
    gap = " ".join(parts[bike_idx + 3 :]) if len(parts) > bike_idx + 3 else None

    return {
        "position": None,
        "points": None,
        "number": number,
        "rider": rider,
        "nation": nation,
        "team": team,
        "bike": bike,
        "total_time": total_time,
        "kmh": kmh,
        "gap": gap if gap else None,
    }


def extract_results(text: str) -> list:
    results = []
    not_classified = False
    for line in text.split("\n"):
        if not line.strip() or line.strip().startswith("Pos"):
            continue
        if line.startswith("Not classified"):
            not_classified = True
            continue
        parts = line.split()
        if not parts:
            continue
        if not_classified:
            entry = parse_non_classified(parts)
        else:
            entry = parse_classified(parts)
        if entry:
            results.append(entry)
    return results


def main() -> None:
    url = "https://resources.motogp.com/files/results/2025/CZE/MotoGP/RAC/Session.pdf"
    response = requests.get(url, timeout=10)
    with pdfplumber.open(io.BytesIO(response.content)) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        results = extract_results(text)
    with Path("data/results/gbr_results.json").open(mode="w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
