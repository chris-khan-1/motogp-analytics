import io
import json
from pathlib import Path

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
    classified_rider_race_info: list[str],
) -> list[dict]:
    results = []
    for line in classified_rider_race_info:
        parts = line.split()
        results.append(
            {
                "position": int(parts[0]),
                "points": int(parts[1]),
                "rider_number": int(parts[2]),
                # "rider": rider,
                # "nation": nation,
                # "team": team,
                # "bike": bike,
                # "total_time": total_time,
                # "kmh": kmh,
                # "gap": gap if gap != "-" else None,
            }
        )
    return results


def extract_non_classified_rider_race_results(
    classified_rider_race_info: list[str],
) -> list[dict]:
    results = []
    for line in classified_rider_race_info:
        parts = line.split()
        results.append(
            {
                "position": None,
                "points": None,
                "rider_number": int(parts[0]),
                # "rider": rider,
                # "nation": nation,
                # "team": team,
                # "bike": bike,
                # "total_time": total_time,
                # "kmh": kmh,
                # "gap": gap if gap != "-" else None,
            }
        )
    return results


def extract_race_results_from_text(text: str) -> list[dict]:
    pass


def find_nation_index(parts: list[str], start_idx: int) -> int | None:
    """Find index of three-letter nation code."""
    for i in range(start_idx, len(parts)):
        if len(parts[i]) == 3 and parts[i].isupper():
            return i
    return None


# def find_bike_index(parts: list[str], start_idx: int, end_idx: int) -> int | None:
#     """Find index of bike manufacturer (all caps)."""
#     for i in range(end_idx, start_idx, -1):
#         if parts[i].isupper() and len(parts[i]) > 3:
#             return i
#     return None


# def parse_time_and_gap(
#     parts: list[str], bike_idx: int
# ) -> tuple[str, float, str | None]:
#     """Extract time, speed and gap."""
#     total_time = parts[bike_idx + 1]
#     try:
#         kmh = float(parts[bike_idx + 2])
#     except (ValueError, IndexError):
#         kmh = 0.0
#     gap = " ".join(parts[bike_idx + 3 :]) if len(parts) > bike_idx + 3 else None
#     return total_time, kmh, gap


# def parse_rider(parts: list[str], start_idx: int, nation_idx: int) -> dict:
#     """Create rider result dictionary."""
#     try:
#         position = int(parts[0]) if parts[0].isdigit() else None
#         points = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else None
#         number = int(parts[start_idx - 1])
#     except (ValueError, IndexError):
#         return None

#     rider = " ".join(parts[start_idx:nation_idx])
#     nation = parts[nation_idx]

#     bike_idx = find_bike_index(parts, nation_idx, len(parts) - 3)
#     if not bike_idx:
#         return None

#     team = " ".join(parts[nation_idx + 1 : bike_idx])
#     total_time, kmh, gap = parse_time_and_gap(parts, bike_idx)

#     return {
#         "position": position,
#         "points": points,
#         "number": number,
#         "rider": rider,
#         "nation": nation,
#         "team": team,
#         "bike": parts[bike_idx],
#         "total_time": total_time,
#         "kmh": kmh,
#         "gap": gap,
#     }


# def parse_classified(parts: list[str]) -> dict | None:
#     """Parse a classified rider's result."""
#     if not parts or len(parts) < 10:
#         return None

#     start_idx = 3 if parts[1].isdigit() else 2
#     nation_idx = find_nation_index(parts, start_idx)

#     if not nation_idx:
#         return None

#     return parse_rider(parts, start_idx, nation_idx)


# def parse_non_classified(parts: list[str]) -> dict | None:
#     """Parse a non-classified rider's result."""
#     if not parts or len(parts) < 8:
#         return None

#     nation_idx = find_nation_index(parts, 1)
#     if not nation_idx:
#         return None

#     result = parse_rider(parts, 1, nation_idx)
#     if result:
#         result["position"] = None
#         result["points"] = None
#     return result


# def extract_results(text: str) -> list:
#     """Extract all results from PDF text."""
#     results = []
#     not_classified = False

#     for line in text.split("\n"):
#         if not line.strip() or line.startswith("Pos"):
#             continue
#         if line.startswith("Not classified"):
#             not_classified = True
#             continue

#         parts = line.split()
#         parser = parse_non_classified if not_classified else parse_classified
#         if result := parser(parts):
#             results.append(result)

#     return results


# def main() -> None:
# url = "https://resources.motogp.com/files/results/2025/CZE/MotoGP/RAC/Session.pdf"
# response = requests.get(url, timeout=10)
# with pdfplumber.open(io.BytesIO(response.content)) as pdf:
#     first_page = pdf.pages[0]
#     text = first_page.extract_text()
#     print(text)
#         results = extract_results(text)
#     with Path("data/results/gbr_results.json").open(mode="w") as f:
#         json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    url = "https://resources.motogp.com/files/results/2023/GBR/MotoGP/RAC/Session.pdf"
    response = requests.get(url, timeout=10)
    with pdfplumber.open(io.BytesIO(response.content)) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        print(text)
#     main()
