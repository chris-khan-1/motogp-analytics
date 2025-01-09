from pprint import pprint

from app.utils.web_scraping import get_event_data_for_year

events_data = get_event_data_for_year(year="2024")

# Print the extracted data
# print("Events Data:")
# for event in events_data:
#     print(event)
pprint(events_data)
