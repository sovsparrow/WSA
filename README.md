# Web Scraping App
## Introduction

This Python project aims to scrape the 1-week weather forecast for the 81 provinces of Turkey from various weather websites. The project utilizes web scraping techniques with Selenium and BeautifulSoup for different weather websites.

## Project Structure

The project is organized into the following components:

- `weather_scraping_app.py`: The main Python script containing the weather scraping logic.
- `Weather_Scraping_App.ipynb`: The Python script as a notebook file with steps.
- `TR_metoffice` and `TR`: Dictionaries mapping plate numbers to city names and vice versa.
- `get_weather_weather`, `get_weather_metoffice`, `get_weather_havadurumux`: Functions to scrape weather data from different websites.
- `DB`: List to store the scraped weather data.

## Dependencies

Ensure you have the following dependencies installed:

- `beautifulsoup4`
- `pymongo`
- `tqdm`
- `requests`
- `selenium`
- `webdriver_manager`

Install the dependencies using:

```bash
pip install -r requirements.txt
Usage
Clone the repository:

```bash
Copy code
git clone https://github.com/your-username/turkey-weather-scraper.git
cd turkey-weather-scraper
Install the required Python packages:

```bash
Copy code
pip install -r requirements.txt
Adjust the parameters in the code if needed, such as the max_workers and max_retries.

Run the scraper:

```bash
Copy code
python weather_scraper.py
The scraper will gather the 1-week weather forecast for the 81 provinces of Turkey from various websites and store the data in the MongoDB database.

View the scraped data:

The scraped weather data is stored in the MongoDB database. You can now use this data for further analysis, visualization, or any other application.

Record Format
The scraped data is stored in the list  with the following fields:
provincial_plate: Plate number of the province.
date: Date of the weather forecast.
weather: Weather data from different sources (metoffice, weather_com, havadurumux) including high and low temperatures.
Acknowledgments
Solo.
