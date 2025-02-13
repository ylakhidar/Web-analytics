import requests
from bs4 import BeautifulSoup
import csv

def extract_all_reviews(base_url, brand, pages):
    headers = {'User-Agent': 'Mozilla/5.0'}
    reviews = []

    for i in range(1, pages + 1):
        url = f"{base_url}?page={i}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Erreur lors de la récupération de la page {i} pour {brand}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        review_containers = soup.select('article[class^="paper_paper__"]')

        for container in review_containers:
            rating_tag = container.select_one('[data-service-review-rating]')
            rating = int(rating_tag['data-service-review-rating']) if rating_tag else None

            if rating is not None and rating <= 3:
                review_content_tag = container.select_one('section[class^="styles_reviewContentwrapper"] p')
                review_content = review_content_tag.text.strip() if review_content_tag else "Non trouvé"

                date_experience_tag = container.select_one('p[data-service-review-date-of-experience-typography="true"]')
                if date_experience_tag:
                    date_experience_text = date_experience_tag.text.strip()
                    date_experience = date_experience_text.split(": ")[-1].strip()
                else:
                    date_experience = "Non trouvé"

                reviews.append({
                    'brand': brand,
                    'rating': rating,
                    'review': review_content,
                    'date_experience': date_experience
                })

    return reviews

# URLs et extraction
pages_to_scrape = 80
total_reviews = []
brands = ["shein", "temu", "amazon"]

for brand in brands:
    total_reviews.extend(extract_all_reviews(f"https://fr.trustpilot.com/review/www.{brand}.com", brand.capitalize(), pages_to_scrape))

# Sauvegarde dans un fichier CSV
csv_filename = "reviews.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['brand', 'rating', 'review', 'date_experience']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(total_reviews)

print(f"Les avis ont été sauvegardés dans {csv_filename}")
