import requests
from bs4 import BeautifulSoup
import pandas as pd

#Best seller url
url = 'https://store.steampowered.com/search/?filter=topsellers'

response = requests.get(url)

#Check if conn was successful
if response.status_code == 200:

    soup = BeautifulSoup(response.content, 'html.parser')

    #Top 15 games
    games = soup.find_all('a', class_='search_result_row', limit=15)

    #List to store game data
    game_data = []

    #Loop for game stats
    for game in games:
        #Game name
        game_name = game.find('span', class_='title').text

        # Base value if error
        price = "Price not available"
        discount = "No discount"

        #Discount
        discount_percent = game.find('div', class_='discount_pct')
        if discount_percent:
            discount = discount_percent.text.strip()
            discount_numeric = int(discount.strip('%'))
        else:
            discount_numeric = 0  

        #Price
        price_div = game.find('div', class_='discount_prices')
        if not price_div:
            price_div = game.find('div', class_='game_purchase_price price')

        if price_div:
            price_text = price_div.text.strip()
            if 'Free' in price_text:
                price = 'Free'
                price_numeric = 0.0
            else:
                #Removing currency symbols
                price = price_text.replace('$', '').strip()
                price_numeric = float(price) if price.replace('.', '', 1).isdigit() else 0.0
        else:
            price_numeric = 0.0  #Default if price is not available

        #Rating
        rating_div = game.find('span', class_='search_review_summary')
        if rating_div:
            rating = rating_div['data-tooltip-html'].split('<br>')[0]
        else:
            rating = "No rating"

        #Append the data to the list
        game_data.append({
            'Game Name': game_name,
            'Price': price,
            'Discount (%)': discount_numeric,
            'Rating': rating
        })

    #Convert the list to a dataframe
    df = pd.DataFrame(game_data)

    #Save dataframe to an Excel file
    df.to_excel('steam_top_sellers.xlsx', index=False)

    print("Data saved to steam_top_sellers.xlsx")



else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")