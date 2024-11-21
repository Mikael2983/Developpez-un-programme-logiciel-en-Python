import re
from io import BytesIO
from pathlib import Path
import csv

import requests
from bs4 import BeautifulSoup
from PIL import Image

class Book:

    def __init__(self, category_name, book_url):
        self.product_page_url = "https://books.toscrape.com/catalogue/" + book_url.replace("../", "")
        self.page = requests.get(self.product_page_url)
        self.soup = BeautifulSoup(self.page.content, "html.parser")
        self.category = category_name

        # Initialize attributes using helper methods
        self.title = self.scrape_title()
        self.universal_product_code = self.scrape_table("UPC")
        self.price_including_tax = self.scrape_table("Price (incl. tax)")
        self.price_excluding_tax = self.scrape_table("Price (excl. tax)")
        self.number_available = self.scrape_availability()
        self.product_description = self.scrape_description()
        self.review_rating = self.scrape_rating()
        self.image_url = self.scrape_image()

    def scrape_title(self):
        product_title = self.soup.find("div", class_="col-sm-6 product_main")
        return product_title.h1.string if product_title else "No title"

    def scrape_table(self, product_item):
        rows = self.soup.find_all("tr")
        for row in rows:
            key = row.find("th").string  # Extract text from <th>
            value = row.find("td").string  # Extract text from <td>
            if key == product_item:
                return value
        return "Not available"

    def scrape_availability(self):
        availability_text = self.scrape_table("Availability")
        match = re.search(r"\d+", availability_text)
        return match.group() if match else "0"

    def scrape_description(self):
        description_tag = self.soup.find_all("p", class_="")
        return description_tag[0].string if description_tag else "No description"

    def scrape_rating(self):
        ratings = {"Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        rating_tag = self.soup.find("p", class_="star-rating")
        if rating_tag and "class" in rating_tag.attrs:
            return ratings.get(rating_tag.get("class")[1], 0)
        return 0

    def scrape_image(self):
        img_tag = self.soup.find("img")
        if img_tag and "src" in img_tag.attrs:
            img_url = img_tag["src"]
            base_url = "https://books.toscrape.com/"
            return base_url + img_url.replace("../", "") if img_url.startswith("../") else img_url
        return "No image available"
        
class Category:
    
    def __init__(self, name=str,url_category=str):
        self.name= name
        self.url= url_category
        self.list = self.scrape_url_books()
    def scrape_url_books(self):
        """
        scrape the urls of all book of the category
        : return: list_url
        """
        page_next = (
        "index.html"  # seconde partie de l'url pour la premiere page de la catégorie.
        )
        page = requests.get(self.url + page_next)
        
        soup = BeautifulSoup(page.content, "html.parser")
        page_number_li = soup.find("li", class_="current")
        list_url=[]
        if page_number_li:
            page_number = page_number_li.get_text(strip=True).split(" ")[-1]
        else:
            page_number = "1"

        for i in range(int(page_number)):
            url = (
                self.url + page_next
            )  # reconstitution de URL en fonction de la page suivante trouvée.
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")

            # extraire la liste des Urls des livres de la catégorie
            list_books = soup.find_all("div", class_="image_container")
            for product in list_books:
                list_a = product.find("a")
                url_book = list_a.get("href")
                list_url.append(url_book)

            page_next = "page-" + str(2 + i) + ".html"  # affichage de la page suivante
        return list_url
        
class Librairy:

    def __init__(self, site_url=str):
        self.site_url = site_url
        self.url_categories = self.scrape_category()

    def scrape_category (self):
        """
        scrape url categories from the web site
        :param :
        :return: url_category 
        """
        page = requests.get(self.site_url)
        soup = BeautifulSoup(page.content, "html.parser")
        url_categories = {}
        categories_div = soup.find(
            "ul", class_="nav-list"
        )
        categories = categories_div.find_all("a")
        for category in categories:  # stockage des url dans un dictionnaire  "nom de la catéorie" = "url de la catégorie"
            url_categories[category.getText().strip()] = self.site_url + category.get(
                "href"
            ).replace("index.html", "")
        del url_categories[
            "Books"
        ]  # cette catégorie n'en est pas réellement une car regroupe tous les livres du site

        return url_categories

def save_cover_picture(book=Book):
    """
    download and save the book cover image
    :param data_book:
    :return:
    """
    picture_file = requests.get(book.image_url)
    picture = Image.open(BytesIO(picture_file.content))
    picture_name = (
            "data/"
            + book.category
            + "/images/"
            + re.sub(r'[\\/*?:"<>|]', " ", book.title)
            + "-"
            + book.universal_product_code
            + ".jpg"
    )
    picture.save(picture_name)


def write_data_on_csv(books=list, category_name=str):
    """
    write data from books of one category to a cvs file
    :param book:
    :param category_name:
    :return:
    """
    # Initialisation du fichier CSV avec le header
    csv_path = Path("data/" + category_name + "/" + category_name + " category book.csv").resolve()
    with open(csv_path, 'w', encoding='utf-8', newline='') as backup_file:
        writer = csv.writer(backup_file, delimiter=",")
        writer.writerow(
            ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
             "number_available", "product_description", "category", "review_rating", "image_url"])

        # Inscription des données de chaque livre
        for book in books:
            print("j'écris le livre " + book.title + " dans le CSV")  
            writer.writerow([
                book.product_page_url,
                book.universal_product_code,
                book.title,
                book.price_including_tax,
                book.price_excluding_tax,
                book.number_available,
                book.product_description,
                book.category,
                book.review_rating,
                book.image_url
            ])