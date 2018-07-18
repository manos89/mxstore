import scrapy
from scrapy.loader import ItemLoader

from mxstore.items import MxstoreItem
import string,unicodedata

all_letters = string.ascii_letters + " .,;'://!#"+string.digits+'"'
n_letters = len(all_letters)

def unicodeToAscii(s):
	return ''.join(c for c in unicodedata.normalize('NFD', unicode(s)) if unicodedata.category(c) != 'Mn' and c in all_letters)

def get_urls():
    base_url="https://mxstore.gr/index.php?route=product/product&product_id={ID}"
    return [base_url.replace("{ID}",str(i)) for i in range(1,10000)]




class QuotesSpider(scrapy.Spider):
    name = "mxstore"

    def start_requests(self):
        urls =  get_urls()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        url=response.request.url
        # CaseReference=response.css("p#Bo_CaseReference::text").extract_first()
        Name=response.xpath('//*[@id="content"]/h1/text()').extract_first()
        Manufacturer=response.xpath('//*[@id="product"]/ul[1]/li[1]/a/text()').extract_first()
        imageclass=response.css('div.image-gallery')[0]
        Images=imageclass.css('img').xpath('@src').extract()
        Images=list(set(Images))
        Images=','.join(Images)
        Price=response.css('li.product-price::text').extract_first()
        Price=unicodeToAscii(Price)
        DesccriptionClass=response.css('div#tab-description')[0]
        Desccription=DesccriptionClass.css('p::text').extract_first()
        l = ItemLoader(item=MxstoreItem(), response=response)
        l.add_value( 'url',url)
        l.add_value( 'name',Name)
        l.add_value( 'manufacturer',Manufacturer)
        l.add_value('price',Price)
        l.add_value('description',Desccription)
        l.add_value( 'images',Images)
        print('DONE ',url)
        # l.add_css('case_reference', 'p#Bo_CaseReference::text')
        # l.add_css('bnkrptc_type', 'p#Bo_BankruptcyType::text')
        return l.load_item()
