import io

import pdfplumber
import requests


def split_classified_and_non_classified(text: str) -> tuple[list[str], list[str]]:
    classified = []
    non_classified = []

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    in_classified_section = False
    in_non_classified_section = False

    for line in lines:
        if line.lower().startswith("pos pts # rider"):
            in_classified_section = True
            continue
        if line.lower().startswith("not classified"):
            in_classified_section = False
            in_non_classified_section = True
            continue

        if in_classified_section:
            classified.append(line)
        elif in_non_classified_section:
            if line and line[0].isdigit():
                non_classified.append(line)
            else:
                break  # stop when non-classified is no longer numbers

    return classified, non_classified


def extract_classified_rider_race_results(
    classified_rider_race_info: str,
) -> dict[str, str | int | float | None]:
    parts = classified_rider_race_info.split()

    position = parts[0]
    points = parts[1]
    rider_number = parts[2]

    # Find the index of the nation code (3 uppercase letters)
    nation_idx = next(i for i, p in enumerate(parts) if len(p) == 3 and p.isupper())

    # Rider name is from index 3 to before the nation code
    rider_name = " ".join(parts[3:nation_idx])
    nation = parts[nation_idx]

    # Motorcycle manufacturer is the last ALL CAPS word before the time
    time_idx = next(i for i, p in enumerate(parts) if "'" in p)
    manufacturer_idx = time_idx - 1

    team_name = " ".join(parts[nation_idx + 1 : manufacturer_idx])
    motorcycle = parts[manufacturer_idx]

    total_time = parts[time_idx]
    speed = parts[time_idx + 1]

    gap = " ".join(parts[time_idx + 2 :]) if time_idx + 2 < len(parts) else None

    return {
        "position": int(position),
        "points": int(points),
        "rider_number": int(rider_number),
        "rider": rider_name,
        "nation": nation,
        "team": team_name,
        "bike": motorcycle,
        "total_time": total_time,
        "kmh": float(speed),
        "gap": gap,
    }


if __name__ == "__main__":
    url = "https://resources.motogp.com/files/results/2023/GBR/MotoGP/RAC/Session.pdf"
    response = requests.get(url, timeout=10)
    with pdfplumber.open(io.BytesIO(response.content)) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
