# PropStore Scraper

## Description
PropStore Scraper is a Python script using Selenium and BeautifulSoup to scrape data from the PropStore website. It logs in, scrolls through the product listings, 
and extracts relevant information, including movie name, price(either sold at for archived items or price offered for live items) from each prop.

## Prerequisites
- Python 3.x
- Chrome Browser
- ChromeDriver (Ensure it's in your system PATH or provide its path)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/propstore-scraper.git
   cd propstore-scraper
   
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Configure ChromeDriver:
Download the appropriate version of ChromeDriver based on your Chrome browser version from ChromeDriver Downloads.

Update chromedriver_path variable in the script (script.py) with the path to your ChromeDriver executable.

Usage
Run the script by executing the following command:

bash
Copy code
python script.py
Configuration
Adjust sleep times in the script based on your network speed and website responsiveness.
Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

License
MIT

arduino
Copy code

Remember to replace the placeholder repository URL (`https://github.com/yourusername/propstore-scraper.git`) with the actual URL of your repository. Adjust the content based on your preferences and project d