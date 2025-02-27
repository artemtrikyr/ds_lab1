import scrapy

from lab2.items import DepartmentItem, FacultyItem, StaffItem


class LnuSpider(scrapy.Spider):
    name = "lnu_css"
    allowed_domains = ["lnu.edu.ua"]
    start_urls = ["https://lnu.edu.ua/about/faculties/"]

    def parse(self, response):
        fac_list =response.css("structural-units")
        for item in fac_list:
            fac_name = item.css("h2::text")
            fac_url = item.css("a::attr(href)")
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
        dep_list = response.css("article.content.divisions")
        for section in dep_list.css("section"):
            a_tag = section.css("h2 a")
            dep_name = a_tag.css("::text")
            dep_url = a_tag.css("::attr(href)").get()

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
        for row in response.css("table tr"):
            name = row.css("tr.name::text").get()            
            if name:
                yield StaffItem(
                    name=name,
                    departament=response.meta.get("departament")
                )
