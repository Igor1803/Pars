import scrapy
from scrapy.exporters import CsvItemExporter

class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/potolocnye-svetilniki"]

    # Настройки для экспорта в CSV
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'divan_data.csv',
        'FEED_EXPORT_FIELDS': ['name', 'price', 'url'],  # Порядок колонок
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        divans = response.css('div._Ud0k')
        for divan in divans:
            # Обработка отсутствующих данных
            yield {
                'name': divan.css('div.lsooF span::text').get() or 'Нет названия',
                'price': divan.css('div.pY3d2 span::text').get().replace(' ', '') if divan.css('div.pY3d2 span::text').get() else '0',
                'url': response.urljoin(divan.css('a::attr(href)').get())
            }