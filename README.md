# Web Scraping App
## Introduction

This Python project aims to scrape the 1-week weather forecast for the 81 provinces of Turkey from various weather websites. The project utilizes web scraping techniques with Selenium and BeautifulSoup for different weather websites.

## Project Structure

The project is organized into the following components:

- `weather_scraper.py`: The main Python script containing the weather scraping logic.
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
