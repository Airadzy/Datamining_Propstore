# PropStore Scraper

## Owners
Adrian: https://www.linkedin.com/in/adrianradzyminski/
Nick: https://www.linkedin.com/in/nickmishkin/

## Description
PropStore Scraper is a Python script using Selenium and BeautifulSoup to scrape data from the PropStore website (https://propstore.com/) which shows historic prices paid and current listings for prop items from film & music. It uses a combination of Selenium and beautifulsoup to log in, scroll through the product listings, 
and extract relevant information, including movie name, price(either sold at for archived items or price offered for live items) from each prop.

## Prerequisites
- Python 3.x
- Chrome Browser (or alternatively specify Browser in driver)
- ChromeDriver (Ensure it's in your system PATH)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Airadzy/Datamining_Propstore.git
   
2. Install dependencies:

   ```bash 
   pip install -r requirements.txt

3. Configure ChromeDriver:
Download the appropriate version of ChromeDriver based on your Chrome browser version from ChromeDriver Downloads.

4. Create Propstore log-in details and update in config.json file
On Propstore.com, create a username and password and update the config.json file with those

## Usage
Run the script by executing the following command:
   
   ```bash 
   python script.py
   ```

## ERD

### Table items:

item_id (integer primary key): A unique identifier for each item. As a primary key, it uniquely identifies each record in the table.

item_description (varchar(255)): A textual description of the item. It can contain up to 255 characters.

category_id (integer): A foreign key that references the category_id in the categories table. This establishes a relationship between each item and its category.

status_id (integer): A foreign key linking to the status_id in the selling_status table. This represents the status of the item (e.g., sold, available).

movie_id (integer): A foreign key that references the movie_id in the movies table, linking the item to a specific movie.

price (decimal(10, 2)): The price of the item. It's a decimal value with 10 digits in total and 2 digits after the decimal point.

currency_id (integer): A foreign key to the currency_id in the currencies table, indicating the currency of the price.

### Table movies:

movie_id (integer primary key): A unique identifier for each movie.

title (varchar(100)): The title of the movie, with a maximum length of 100 characters.

### Table categories:

category_id (integer primary key): A unique identifier for each category.

category (varchar(100)): The name or type of the category, with a maximum length of 100 characters.

### Table currencies:

currency_id (integer primary key): A unique identifier for each currency.

currency (varchar(3)): The ISO code for the currency, such as 'USD' for US Dollars, 'GBP' for British Pounds, etc., with a maximum length of 3 characters.

### Table selling_status:

status_id (integer primary key): A unique identifier for each status.

status_description (varchar(50)): A textual description of the status (e.g., 'Buy Now', 'Just Sold'), with a maximum length of 50 characters.

sold_date (date): The date on which the item was sold. This field stores dates in the format YYYY-MM-DD.


![PropStore Scraper (3)](https://github.com/Airadzy/Datamining_Propstore/assets/114605683/c0dae16a-a2e4-441f-a7a1-b600fb53b1f8)

