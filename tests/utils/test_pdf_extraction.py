# @pytest.fixture
# def classified_rider():
#     return [
#         "1",
#         "25",
#         "93",
#         "Marc",
#         "MARQUEZ",
#         "SPA",
#         "Ducati",
#         "Lenovo",
#         "Team",
#         "DUCATI",
#         "40'04.628",
#         "169.8",
#     ]


# @pytest.fixture
# def non_classified_rider():
#     return [
#         "21",
#         "Alex",
#         "MARQUEZ",
#         "SPA",
#         "Gresini",
#         "Racing",
#         "MotoGP",
#         "DUCATI",
#         "40'35.000",
#         "167.5",
#         "31.000",
#     ]


# def test_find_nation_index():
#     parts = ["Marc", "MARQUEZ", "SPA", "Team"]
#     assert find_nation_index(parts, 0) == 2
#     assert find_nation_index(parts, 3) is None


# def test_find_bike_index():
#     parts = ["Team", "DUCATI", "40'04.628"]
#     assert find_bike_index(parts, 0, 2) == 1
#     assert find_bike_index(["Team", "Racing"], 0, 1) is None


# def test_parse_time_and_gap():
#     parts = ["DUCATI", "40'04.628", "169.8", "1.234"]
#     time, speed, gap = parse_time_and_gap(parts, 0)
#     assert time == "40'04.628"
#     assert speed == 169.8
#     assert gap == "1.234"


# def test_parse_classified_complete(classified_rider):
#     result = parse_classified(classified_rider)
#     assert result["position"] == 1
#     assert result["points"] == 25
#     assert result["number"] == 93
#     assert result["rider"] == "Marc MARQUEZ"
#     assert result["nation"] == "SPA"
#     assert result["team"] == "Ducati Lenovo Team"
#     assert result["bike"] == "DUCATI"
#     assert result["total_time"] == "40'04.628"
#     assert result["kmh"] == 169.8
#     assert result["gap"] is None


# def test_parse_classified_no_points():
#     parts = ["16", "Fabio", "DI", "GIANNANTONIO", "ITA"]
#     result = parse_classified(parts)
#     assert result is None  # Invalid format should return None


# def test_parse_non_classified_complete(non_classified_rider):
#     result = parse_non_classified(non_classified_rider)
#     assert result["position"] is None
#     assert result["points"] is None
#     assert result["number"] == 21
#     assert result["rider"] == "Alex MARQUEZ"
#     assert result["bike"] == "DUCATI"


# def test_extract_results_mixed():
#     text = """Pos Pts # Rider Nation Team Motorcycle Total Time Km/h Gap
# 1 25 93 Marc MARQUEZ SPA Ducati Lenovo Team DUCATI 40'04.628 169.8
# Not classified
# 21 Alex MARQUEZ SPA Gresini Racing MotoGP DUCATI 40'35.000 167.5 31.000"""

#     results = extract_results(text)
#     assert len(results) == 2
#     assert results[0]["position"] == 1
#     assert results[1]["position"] is None


# def test_extract_results_full():
#     text = """Updated
# i1
# CLASSIFICATION AFTER 21 LAPS = 113.463 KM
# i2
# TISSOT GRAND PRIX OF CZECHIA s fl i3
# RACE
# Automotodrom Brno 5403 m.
# Pos Pts # Rider Nation Team Motorcycle Total Time Km/h Gap
# 1 25 93 Marc MARQUEZ SPA Ducati Lenovo Team DUCATI 40'04.628 169.8
# 2 20 72 Marco BEZZECCHI ITA Aprilia Racing APRILIA 40'06.381 169.7 1.753
# 3 16 37 Pedro ACOSTA SPA Red Bull KTM Factory Racing KTM 40'07.994 169.6 3.366
# 4 13 63 Francesco BAGNAIA ITA Ducati Lenovo Team DUCATI 40'08.507 169.5 3.879
# 5 11 25 Raul FERNANDEZ SPA Trackhouse MotoGP Team APRILIA 40'14.673 169.1 10.045
# 6 10 20 Fabio QUARTARARO FRA Monster Energy Yamaha MotoGP Team YAMAHA 40'15.667 169.0 11.039
# 7 9 1 Jorge MARTIN SPA Aprilia Racing APRILIA 40'20.448 168.7 15.820
# 8 8 33 Brad BINDER RSA Red Bull KTM Factory Racing KTM 40'21.999 168.6 17.371
# 9 7 44 Pol ESPARGARO SPA Red Bull KTM Tech3 KTM 40'22.791 168.5 18.163
# 10 6 43 Jack MILLER AUS Prima Pramac Yamaha MotoGP YAMAHA 40'23.297 168.5 18.669
# 11 5 54 Fermin ALDEGUER SPA BK8 Gresini Racing MotoGP DUCATI 40'24.409 168.6 19.781
# 12 4 10 Luca MARINI ITA Honda HRC Castrol HONDA 40'25.406 168.4 20.778
# 13 3 5 Johann ZARCO FRA CASTROL Honda LCR HONDA 40'25.589 168.3 20.961
# 14 2 79 Ai OGURA JPN Trackhouse MotoGP Team APRILIA 40'26.532 168.3 21.904
# 15 1 42 Alex RINS SPA Monster Energy Yamaha MotoGP Team YAMAHA 40'27.191 168.2 22.563
# 16 49 Fabio DI GIANNANTONIO ITA Pertamina Enduro VR46 Racing Team DUCATI 40'29.357 168.1 24.729
# 17 88 Miguel OLIVEIRA POR Prima Pramac Yamaha MotoGP YAMAHA 40'32.268 167.9 27.640
# 18 7 Augusto FERNANDEZ SPA Yamaha Factory Racing Team YAMAHA 40'32.938 167.8 28.310
# Not classified
# 23 Enea BASTIANINI ITA Red Bull KTM Tech3 KTM 11'33.792 168.2 15 laps
# 36 Joan MIR SPA Honda HRC Castrol HONDA 2'00.704 161.1 20 laps
# 73 Alex MARQUEZ SPA BK8 Gresini Racing MotoGP DUCATI 2'00.801 161.0 20 laps
# Race condition:Dry Pole Position: Francesco BAGNAIA 1'52.303 173.1 Km/h
# Air: 27° Fastest Lap (New record): Lap 15 Marc MARQUEZ 1'53.691 171.0 Km/h
# Humidity: 46% Best Race Lap: 2014 Daniel PEDROSA 1'56.027 167.6 Km/h
# Ground: 40° All-Time Lap Record: 2025 Francesco BAGNAIA 1'52.303 173.1 Km/h
# 13:35'00 SIGHTING LAP START
# 13:59'40 WARM UP LAP START
# 14:04'12 No jump starts
# 14:04'35 Augusto FERNANDEZ long lap penalty
# 14:06'08 Alex MARQUEZ crashed out - Rider OK
# 14:06'17 Joan MIR crashed out - Rider OK
# 14:06'28 Augusto FERNANDEZ long lap penalty - COMPLETE
# 14:14'33 Enea BASTIANINI crashed out - Rider OK
# 14:58'54 Fermin ALDEGUER long lap penalty due to irresponsible riding
# 14:59'56 Fermin ALDEGUER 3 seconds penalty - insufficient time to complete long lap penalty
# The results are provisional until the end of the limit for protest and appeals.
# Jindrich Hrnecek 15:19
# Time limit for protest expires 60' after publication of the results - ................................................................................................................................................................ Time: ............................
# These data/results cannot be reproduced, stored and/or transmitted in whole or in part by any manner of electronic, mechanical, photocopying, recording, broadcasting or otherwise
# now known or herein after developed without the previous express consent by the copyright owner, except for reproduction in daily press and regular printed publications on sale to
# the public within 60 days of the event related to those data/results and always provided that copyright symbol appears together as follows below.
# © DORNA, 2025
# Official MotoGP Timing by
# www.motogp.com
# Brno, Sunday, July 20, 2025"""

#     results = extract_results(text)
#     print(results)
