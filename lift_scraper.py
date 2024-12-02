import requests
from bs4 import BeautifulSoup

# Makes a GET request to the website to access its content
r = requests.get("https://iwf.sport/results/results-by-events/?event_id=604")

soup = BeautifulSoup(r.content, 'html.parser')

# Find the div with the id 'men_snatchjerk'
s = soup.find('div', attrs={'id': 'men_snatchjerk'})

# Find all divs with the class 'cards' within the 's' section
mens_cards = s.find_all('div', class_="card")

# Initialize a list to hold all data
card_data = []

# print(mens_cards)

# print(a)
# Loop through each 'cards' div and extract rows with 'row no-gutters'
for card in mens_cards:
    rows = card.find_all("div", class_="row no-gutters")
    for row in rows:
        # Extract rank
        rank_span = row.find('span', string="Rank:")
        rank = rank_span.find_next_sibling(text=True).strip() if rank_span and rank_span.find_next_sibling() else "---"
        
        # Extract name
        name_div = row.find('div', class_="col-7 not__cell__767")
        name = name_div.get_text(strip=True) if name_div else "---"
        
        # Extract date of birth
        dob_div = row.find('p', class_="normal__text")
        dob_span = dob_div.find('span', class_="only__mobile") if dob_div else None
        date_of_birth = dob_span.find_next_sibling(text=True).strip() if dob_span and dob_span.find_next_sibling() else "---"
        
        # Extract body weight
        weight_div = row.find('div', class_="col-4 not__cell__767")
        weight_span = weight_div.find('span', string="B.weight:") if weight_div else None
        weight = weight_span.find_next_sibling(text=True).strip() if weight_span and weight_span.find_next_sibling() else "---"
        
        # Extract snatch attempts
        snatch_1_span = row.find('span', string="1:")
        snatch_1 = snatch_1_span.find_next_sibling('strong').get_text(strip=True) if snatch_1_span and snatch_1_span.find_next_sibling('strong') else "---"
        
        snatch_2_span = row.find('span', string="2:")
        snatch_2 = snatch_2_span.find_next_sibling('strong').get_text(strip=True) if snatch_2_span and snatch_2_span.find_next_sibling('strong') else "---"
        
        snatch_3_span = row.find('span', string="3:")
        snatch_3 = snatch_3_span.find_next_sibling('strong').get_text(strip=True) if snatch_3_span and snatch_3_span.find_next_sibling('strong') else "---"
        
        # Compile data into a dictionary
        card_data.append({
            'Rank': rank,
            'Name': name,
            'Date of Birth': date_of_birth,
            'Body Weight': weight,
            'Snatch 1': snatch_1,
            'Snatch 2': snatch_2,
            'Snatch 3': snatch_3,
            })

# Output card_data to verify
print("\n------------------------------BIG GAP-------------------------------------------")
for data in card_data:
    print(data)
