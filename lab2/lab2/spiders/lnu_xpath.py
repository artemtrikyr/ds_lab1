import scrapy
from lab2.items import DepartmentItem, FacultyItem, StaffItem


class LnuSpider(scrapy.Spider):
    name = "lnu_xpath"
    allowed_domains = ["lnu.edu.ua"]
    start_urls = ["https://lnu.edu.ua/about/faculties/"]

    def parse(self, response):
        fac_list = response.xpath('//ul[contains(@class, "structural-units")]/li')
        
        for fac in fac_list:
            fac_name = fac.xpath('.//h2/text()').get()
            fac_url = fac.xpath('.//a/@href').get()
            kaf_url = fac_url + "/about/departments"
            
            yield FacultyItem(
                name=fac_name.strip() if fac_name else None,
                url=fac_url
            )
            
            yield scrapy.Request(
                url=kaf_url,
                callback=self.parse_faculty,
                meta={"faculty": fac_name}
            )

    def parse_faculty(self, response):
        dep_list = response.xpath('//article[contains(@class, "content divisions")]/section')
        
        for dep in dep_list:
            dep_name = dep.xpath('.//h2/a/text()').get()
            dep_url = dep.xpath('.//h2/a/@href').get()
            
            yield DepartmentItem(
                name=dep_name.strip() if dep_name else None,
                url=dep_url,
                faculty=response.meta.get("faculty")
            )
            
            yield scrapy.Request(
                url=dep_url,
                callback=self.parse_staff,
                meta={"departament": dep_name}
            )

    def parse_staff(self, response):
        staff_rows = response.xpath('//table//tr')
        
        for row in staff_rows:
            name = row.xpath('.//td[contains(@class, "name")]/text()').get()
            if name:
                yield StaffItem(
                    name=name.strip(),
                    departament=response.meta.get("departament")
                )
