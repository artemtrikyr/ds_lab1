from requests import get
from bs4 import BeautifulSoup

BASE_URL = "https://lnu.edu.ua/"
URL = f"{BASE_URL}about/faculties/"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

FILE_NAME = "lnu.txt"
with open(FILE_NAME, "w", encoding="utf-8") as file:

    page = get(URL, headers=HEADERS)
    soup = BeautifulSoup(page.content, "html.parser")
    fac_list = soup.find(class_="structural-units")

    for li in fac_list.find_all("li"):
        h2 = li.find("h2")
        a = li.find("a")
        fac_name = h2.find(string=True, recursive=False)
        fac_url = a.get("href")

        file.write(f"Назва факультету: {fac_name}")
        file.write(f"Посилання: {fac_url}")

        kaf_url = fac_url + "/about/departments"
        file.write(f"Посилання на кафедри факультету: {kaf_url}")

        #завантажуємо сторінку факультету
        fac_page = get(kaf_url, headers=HEADERS)

        soup = BeautifulSoup(fac_page.content,  "html.parser")
        dep_list = soup.find("article", class_="content divisions")

        for section in dep_list.find_all("section"):
            a_tag = section.find("h2").find("a")
            dep_name = a_tag.get_text(strip=True)
            dep_url = a_tag.get("href")
            file.write(f"  📌Назва кафедри: {dep_name}")
            file.write(f"  🔗URL: {dep_url}")

            #завантажуємо сторінку кафедри
            dep_page = get(f"{dep_url}", headers=HEADERS)
            #знаходимо список викладачів
            soup = BeautifulSoup(dep_page.content,  "html.parser")
            staff_table = soup.find("table")
            #для кожного викладача у списку

            file.write("      Викладачі:")
            for row in staff_table.find_all("tr"):
                name_cell = row.find("td", class_="name")
                if name_cell:
                    name = name_cell.get_text(strip=True)
                    file.write(f"        - {name}")
            file.write(f"-")



        print(f"-" * 50)


