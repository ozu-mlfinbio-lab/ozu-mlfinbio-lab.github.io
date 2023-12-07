import numpy as np
from datetime import datetime

def convert_date(date_str):
    date_object = datetime.strptime(date_str, "%d/%m/%y")
    formatted_date = date_object.strftime("%d %B %Y")
    return formatted_date

def create_html(data):
    html_content = ""
    for i, row in enumerate(data):
        date = convert_date(row[0])
        content = row[1]
        container = "news-first" if i == 0 else "news"
        html_content += f"""        
        <div class="{container}">
            <h4>{date}</h4>
            <p>{content}</p>
        </div>
        """
    return html_content


def sort(data):
    dates = [datetime.strptime(row[0], "%d/%m/%y") for row in data]
    sorted_indices = np.argsort(dates)[::-1]
    return data[sorted_indices]


if __name__ == "__main__":
    csv_file_path = "../assets/news/news.csv"
    data = np.genfromtxt(csv_file_path, delimiter=";", dtype=str, skip_header=1, usecols=(0, 1))
    data = sort(data)
    content = create_html(data)
    with open("news.html", "w", encoding="utf-8") as html_file:
        html_file.write(content)
