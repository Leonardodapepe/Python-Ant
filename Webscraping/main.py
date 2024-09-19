import requests
from bs4 import BeautifulSoup
#Best seller url
url = 'https://store.steampowered.com/search/?filter=topsellers'


response = requests.get(url)

#Check if conn was succsesfull
if response.status_code == 200:
   
    soup = BeautifulSoup(response.content, 'html.parser')

    #takes top 15 games
    games = soup.find_all('a', class_='search_result_row', limit=15)

    #Loop for game stats
    for game in games:
        #Game name
        game_name = game.find('span', class_='title').text

        #Base value incase error
        price = "Price not available"
        discount = "No discount"

        #Discount 
        discount_percent = game.find('div', class_='discount_pct')
        if discount_percent:
            discount = discount_percent.text.strip()

        #Price
        price_div = game.find('div', class_='discount_prices')
        if not price_div:
            price_div = game.find('div', class_='game_purchase_price price')

        if price_div:
            price_text = price_div.text.strip()
            if 'Free' in price_text:
                price = 'Free'
            else:
                price = price_text

        #Rating
        rating_div = game.find('span', class_='search_review_summary')
        if rating_div:
            rating = rating_div['data-tooltip-html'].split('<br>')[0]
        else:
            rating = "No rating"

        #Print stats
        print(f"Game: {game_name}")
        print(f"Price: {price}")
        print(f"Discount: {discount}")
        print(f"Rating: {rating}")
        print("-" * 40)

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")