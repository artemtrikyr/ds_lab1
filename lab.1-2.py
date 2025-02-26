from requests import get
from bs4 import BeautifulSoup

BASE_URL = "https://rozetka.com.ua"
URL = f"{BASE_URL}/mobile-phones/c80003/producer=apple/"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

LAST_PAGE = 13

for p in range(1, LAST_PAGE):
    page = get(URL, headers=HEADERS, params={"p": p})
    soup = BeautifulSoup(page.content,  "html.parser")
    item = soup.find(
        name="div", class_="content_type_catalog", find_all(class_="")
    )