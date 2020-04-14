import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from flask import current_app as app

def parse_data(date_str, content_str):
    pattern = r"Aktuell (\d+) bestätigte Coronafälle in der StädteRegion Aachen \(davon (\d+) in der Stadt Aachen\). (\d+) ehemals positiv auf das Corona-Virus getestete Personen sind inzwischen wieder gesund\. Bislang (\d+) Todesfälle\."

    m = re.match(pattern, content_str)

    if m is None:
        return {}

    reg, city, recov, dead = m.groups()

    date_pattern = r"(\w+), (\d{1,2}).(\d{2}).(\d{4}), (\d{1,2})[:.](\d{2})"
    m = re.match(date_pattern, date_str)
    # print(date_str)

    ## print(reg, city, recov, dead)

    if m is None:
        return {}

    _, day, month, year, hour, minute = m.groups()
    ## print(year, month, day, hour, minute)

    date = datetime(
        int(year),
        int(month),
        int(day),
        int(hour),
        int(minute)
    )

    result = {
        "timestamp": date,
        "cases_region": reg,
        "cases_city": city,
        "recovered": recov,
        "deaths": dead,
        "orig_date_str": date_str,
        "orig_data_str": content_str
    }
    # # print(result)
    return result


def fetch_and_parse_page_data():
    resp = requests.get(app.config["AACHEN_DATA_LINK_FULL"])
    if resp.status_code != 200:
        raise Exception("ExternalPageError")

    html = resp.text

    soup = BeautifulSoup(html, features="html.parser")
    page_contents_div = soup.find('div', 'content')
    content_sections = page_contents_div.find_all("h2")

    results = []
    for section in content_sections:
        # print("Current Node:", section.text)

        nextNode = section
        while True:
            if nextNode is None:
                break

            nextNode = nextNode.next_sibling
            try:
                tag_name = nextNode.name
            except AttributeError:
                tag_name = ""

            if tag_name == "h2":
                # print("*****")
                break
            elif tag_name == "ul":
                text = nextNode.find('li')
                parsed_data = parse_data(section.text, text.text)

                results.append(parsed_data)
                # print("*****")
                break
            else:
                pass

    ## print("Results", results)
    return results