import scrapy
from bs4 import BeautifulSoup

from lab2.items import DepartmentItem, FacultyItem, StaffItem


class LnuSpider(scrapy.Spider):
    name = "lnu"
    allowed_domains = ["lnu.edu.ua"]
    start_urls = ["https://lnu.edu.ua/about/faculties/"]

    def parse(self, response):
        soup = BeautifulSoup(response.body,  "html.parser")
        fac_list = soup.find(class_="structural-units")

        for li in fac_list.find_all("li"):
            h2 = li.find("h2")
            a = li.find("a")
            fac_name = h2.find(string=True, recursive=False)
            fac_url = a.get("href")
            kaf_url = fac_url + "/about/departments"

            yield FacultyItem(
                name=fac_name,
                url=fac_url
            )
            
            yield scrapy.Request(
                url=kaf_url,
                callback=self.parse_faculty,
                meta={
                    "faculty" : fac_name
                }
            )

    def parse_faculty(self, response):
        soup = BeautifulSoup(response.body,  "html.parser")
        dep_list = soup.find("article", class_="content divisions")
        for section in dep_list.find_all("section"):
            a_tag = section.find("h2").find("a")
            dep_name = a_tag.get_text(strip=True)
            dep_url = a_tag.get("href")

            yield DepartmentItem(
                name=dep_name,
                url=dep_url,
                faculty=response.meta.get("faculty")
            )

            yield scrapy.Request(
                url=dep_url,
                callback=self.parse_staff,
                meta={
                    "departament" : dep_name
                }
            )

    def parse_staff(self, response):
        soup = BeautifulSoup(response.body,  "html.parser")
        staff_table = soup.find("table")
        for row in staff_table.find_all("tr"):
            name_cell = row.find("td", class_="name")
            if name_cell:
                name = name_cell.get_text(strip=True)
            yield StaffItem(
                name=name,
                departament=response.meta.get("departament")
            )
