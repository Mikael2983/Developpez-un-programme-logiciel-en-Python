import utils
from pathlib import Path

if __name__ == "__main__":

    url_site = "https://books.toscrape.com/"

    site = utils.Librairy(url_site)
    
    for category_name in site.url_categories:
        category = utils.Category(category_name,site.url_categories[category_name])
        
        repertory = Path("data/" + category.name + "/images").resolve()
        repertory.mkdir(parents=True, exist_ok=True)
        books = []
        
        for url in category.list:
            book= utils.Book(category.name,url)
            utils.save_cover_picture(book)
            books.append(book)

        utils.write_data_on_csv(books,category.name)