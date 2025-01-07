from app.utils.web_scraping import get_event_data_for_year

events_data = get_event_data_for_year(year="1999")

# Print the extracted data
print("Events Data:")
for event in events_data:
    print(event)
