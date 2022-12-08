""" 
Scrapes municipality info from `https://www.gov.za/about-government/contact-directory/provincial-local-government` and store in json file
Example Format of data saved in file:
{
    province:{
        municipality_name:{
            scrape_url: <str>,
            municipality: {
                website: [<str>],
                postal address: [<str>],
                street address: [<str>],
                phone: [<str>],
                fax: [<str>],
                directories: [<str>],
            },
            Executive Mayor: {
                name: <str>,
                postal address: [<str>],
                street address: [<str>],
                phone: [<str>],
                fax: [<str>],
                e-mail: [<str>],
            },
            Municipal Manager: {
                name: <str>,
                postal address: [<str>],
                street address: [<str>],
                phone: [<str>],
                fax: [<str>],
                e-mail: [<str>],
            }
        },
        ...
    },
    ...
}
"""

from bs4 import BeautifulSoup, element
import requests
import json

BASE_URL = "https://www.gov.za"
PAGE_URL = "https://www.gov.za/about-government/contact-directory/provincial-local-government"
PROVINCES = {
    "Eastern Cape": 0,
    "Free State": 1,
    "Gauteng": 2,
    "KwaZulu-Natal": 3,
    "Limpopo": 4,
    "Mpumalanga": 5,
    "North West": 6,
    "Northern Cape": 7,
    "Western Cape": 8,
}


def get_page(session: requests.Session, url: str) -> str:
    """
    Returns the html content of a url
    :param requests.Session session: session used to get page 
    :param str url: page url to get html content from
    :returns: str
    """
    response = session.get(url)
    return response.text


def get_municipality_urls(province: int, html_page: str) -> dict:
    """
    Parses and returns municipality urls from html_page
    :param int province: Number associated with province, range -> 0 - 8. Example 0 = Eastern Cape & 8= Western Cape
    :param str html_page: html_page to scrape municipality urls from
    :returns: dict
    """
    data = {}
    soup = BeautifulSoup(html_page, 'html.parser')
    municipalities = soup.select(
        ".pane-content .sub-directory div.views-row")[province].select(".group-info div")
    for municipality in municipalities:
        muni_link = municipality.select_one("a")
        muni_name = muni_link.text.split(" ")
        muni_name = " ".join(muni_name[:len(muni_name)-2])
        data[muni_name] = {}
        data[muni_name]["scrape_url"] = BASE_URL + muni_link.get("href")
    return data


def is_group_field_item_link(field_item: element.Tag) -> bool:
    """
    Checks if a field item contains an <a> Tag.
    :param element.Tag field_item: field_item element to check <a> Tag in.
    :returns: bool
    """
    return len(field_item.select("a")) > 0


def extract_field_item_link_value(field_item: element.Tag) -> str:
    """
    Extract and returns content of <a> Tag in field_item element
    :param element.Tag field_item: field_item element to extract <a> Tag content from.
    :returns: str
    """
    url = field_item.select_one("a").text
    url = BASE_URL+url if url.startswith("/") else url
    return url


def get_fields_from_group_info(group_info: element.Tag, get_head: bool = True, head: str = " ") -> dict:
    """
    Returns a dictionary containing fields found in group_info element and their values.
    :param element.Tag group_info: Element containing fields.
    :param bool get_head: Get key of data from element (This is true if the element contains an h2 Tag).
    :param str head: Default head used if get_head param is false.
    :returns: dict
    """
    data = {}
    if get_head:
        head_label = group_info.select_one("h2").text.split(":")[0].strip(" ")
        head_value = group_info.select_one("h2 a").getText(
            strip=True).replace("\xa0", " ").replace("        ", " ")
        data[head_label] = {"name": head_value}
    else:
        head_label = head
        data[head_label] = {}

    fields = group_info.select(".field")
    for field in fields:
        field_label = field.select_one(
            ".field-label").text.split(":")[0].strip(" ").lower()
        field_items = field.select(".field-item")
        field_contents = []
        for field_item in field_items:
            field_contents.append(field_item_content(field_item))

        if len(field_items) == 0:
            field_item = field.select_one("div:nth-child(2)")
            field_contents.append(field_item_content(field_item))
        data[head_label][field_label] = field_contents
    return data


def field_item_content(field_item: element.Tag) -> str:
    """
    Returns the text content of a field_item.
    :param element.Tag field_item: Element to get text content from.
    :returns: str
    """
    content = ""
    if is_group_field_item_link(field_item):
        content = extract_field_item_link_value(field_item)
    else:
        if len(field_item.select("li")) > 0:

            content = field_item.select_one("li").getText(strip=True)
        else:
            content = field_item.getText(strip=True)
    return content.replace("\xa0", " ")


def get_municipality_info(session: requests.Session, url: str) -> dict:
    """
    Returns the municipality info scraped from the url provided.
    :param requests.Session session: session used to fetch url.
    :param str url: url to get municipality information from.
    :returns: dict
    """
    data = {}
    html_page = get_page(session, url)
    soup = BeautifulSoup(html_page, 'html.parser')
    groups = soup.select(".group-info")[:3]
    for i, group in enumerate(groups):
        if i == 0:
            data.update(get_fields_from_group_info(
                group, get_head=False, head="municipality"))
        else:
            data.update(get_fields_from_group_info(group, get_head=True))

    return data


def save_data(data: dict):
    """
    Converts data to json and saves in file
    """
    with open("municipality_details/data.json", "w+") as fp:
        fp.write(json.dumps(data))
        fp.close()


if __name__ == "__main__":
    with requests.session() as session:
        html_page = get_page(session, PAGE_URL)
        data = {}
        for province in PROVINCES.keys():
            data[province] = get_municipality_urls(
                PROVINCES[province], html_page)
            print(f"Scraping municipal details in {province} ....")
            for municipality in data[province].keys():
                data[province][municipality].update(get_municipality_info(
                    session, data[province][municipality]["scrape_url"]))
            save_data(data)
            print(f"Completed {data[province].keys()} municipalities")
