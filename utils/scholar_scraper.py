import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_google_scholar(username):
    base_url = f"https://scholar.google.com/citations?user={username}"
    articles = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    session = requests.Session()
    response = session.get(base_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    articles.extend(parse_articles(soup))

    while True:
        next_button = soup.find("button", {"id": "gsc_bpf_more"})
        if next_button:
            next_page_url = base_url + f"&cstart={len(articles)}"
            response = session.get(next_page_url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
            new_articles = parse_articles(soup)
            if not new_articles:
                break
            articles.extend(new_articles)
            delay = random.uniform(1, 3)
            time.sleep(delay)
        else:
            break

    filtered_articles = [article for article in articles if article["year"].isdigit() and "arXiv" not in article["journal"] and "Ozyegin University" not in article["journal"] and len(article["journal"]) > 1]
    sorted_articles_descending = sorted(filtered_articles, key=lambda article: int(article["year"]), reverse=True)
    return sorted_articles_descending

def parse_articles(soup):
    articles = []
    item_list = soup.find_all("tr", {"class": "gsc_a_tr"})
    for article in item_list:
        if article.find("a", {"class": "gsc_a_at"}) and article.find("div", class_="gs_gray") and article.find("div", class_="gs_gray").find_next("div", class_="gs_gray") and article.find("td", {"class": "gsc_a_y"}):
            title = article.find("a", {"class": "gsc_a_at"}).text
            authors = article.find("div", class_="gs_gray").text
            journal = article.find("div", class_="gs_gray").find_next("div", class_="gs_gray").text
            year = article.find("td", {"class": "gsc_a_y"}).text

            articles.append({
                "title": title,
                "authors": authors,
                "journal": journal,
                "year": year
            })

    return articles

def to_html(articles, start_year):
    lab_articles = [article for article in articles if int(article["year"]) >= start_year]
    html_content = f""" 
        <h2>Publications</h2>
        <div class="line"></div>

    """
    paper_id = 0
    articles_by_year = {}

    # Organize articles into lists by year
    for article in lab_articles:
        year = article["year"]
        if year in articles_by_year:
            articles_by_year[year].append(article)
        else:
            articles_by_year[year] = [article]

    # Convert the dictionary values into a list of lists
    yearly_article_dict = articles_by_year

    # Get the sorted list of years
    sorted_years = sorted(yearly_article_dict.keys(), key=int, reverse=True)

    # Iterate over the articles starting from the lowest year
    for year in sorted_years:
        articles_for_year = yearly_article_dict[year]
        
        html_content += f"""

        <h3>{year}</h3> 
        
        """

        for article in articles_for_year:

            title = article["title"]
            authors = article["authors"]
            journal = article["journal"]
            year = article["year"]

            first_letters = [word[0].lower() for word in title.split()]
            thumbnail_name =  ''.join(first_letters)

            html_content += f"""<div class="publication-container">
            <div class="thumbnail-section">
                <img src="assets/publications/{thumbnail_name}.png" alt="Thumbnail">
            </div>
            <div class="info-section">      
                <h3>{title}</h3>
                <p>Published in: {journal}</p>
                <p>Authors: {authors}</p>
                <p>Year: {year}</p>
            </div>
            </div>
        """
    return html_content

if __name__ == "__main__":
    username = "kdJBxv8AAAAJ&hl=en"
    start_year = 2016
    articles = scrape_google_scholar(username)
    articles_html = to_html(articles, start_year=start_year)
    with open("utils/scraped_publications.html", "w", encoding="utf-8") as html_file:
        html_file.write(articles_html)
