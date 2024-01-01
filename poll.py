import csv
import requests
import time
from bs4 import BeautifulSoup

# Function to extract delivery date, combined aircraft manufacturer and model, and year built from the website
def get_aircraft_details_from_website(url):
    try:
        print(f"Fetching data for URL: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            delivery_date = None
            manufacturer = None
            model = None
            aircraft_model = None
            year_built = None

            tables = soup.find_all('table', class_='table table-striped table-condensed')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if cells and len(cells) == 2:
                        label = cells[0].get_text().strip()
                        value = cells[1].get_text().strip()
                        if "Delivery Date:" in label:
                            delivery_date = value
                        elif label == "Manufacturer:":
                            manufacturer = value.split()[0].strip()  # Extracting the first word (manufacturer name)
                        elif label == "Model:":
                            model = value.split()[0].strip()  # Extracting the first word (model name)
                        elif label == "Year built:":
                            year_built = value + "-01-01"

                # Combine manufacturer and model
                if manufacturer and model:
                    aircraft_model = f"{manufacturer} {model}"

                # Use year built as fallback for delivery date
                if not delivery_date and year_built:
                    delivery_date = year_built

                # Break after processing the first record
                break

            if not delivery_date:
                print("Delivery Date not found.")
            if not aircraft_model:
                print("Aircraft Model not found.")

            return delivery_date, aircraft_model
        else:
            print(f"Failed to fetch URL {url}: Status code {response.status_code}")
            return None, None
    except Exception as e:
        print(f"Error fetching data for URL {url}: {e}")
        return None, None

# Read IDs from CSV and write results to a new CSV
input_file = 'input.csv'  # Replace with your input CSV file path
output_file = 'output.csv'  # Replace with your desired output CSV file path

print("Processing IDs...")
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    writer.writerow(['ID', 'Delivery Date', 'Aircraft Model'])

    for row in reader:
        id = row[0]
        url = f'https://www.airport-data.com/aircraft/{id}.html'
        delivery_date, aircraft_model = get_aircraft_details_from_website(url)
        writer.writerow([id, delivery_date, aircraft_model])
        print(f"Processed ID: {id}, Delivery Date: {delivery_date}, Aircraft Model: {aircraft_model}")
        # time.sleep(2)  # Add a delay to prevent rate limiting

print("Data extraction complete.")
