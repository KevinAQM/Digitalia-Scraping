from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from numpy import nan
from bs4 import BeautifulSoup
from lxml import etree
import requests

busqueda = input("¿Qué artículo deseas buscar en Mercado Libre?: ")

class MercadolibreSpider(CrawlSpider):
    name = 'mercadolibre'
    allowed_domains = ['articulo.mercadolibre.com.pe', 'click1.mercadolibre.com.pe', 'listado.mercadolibre.com.pe']
    start_urls = ['https://listado.mercadolibre.com.pe/{}'.format(busqueda)]

    rules = (
        Rule(LinkExtractor(allow='_Desde'), follow=True),
        Rule(LinkExtractor(allow='MPE-'), callback='parse_filter', follow=True),
    )

    def parse_filter(self, response):
        
        titulo = response.xpath("//div[@class='ui-pdp-header__title-container']/h1/text()").get()
        
        link = response.xpath("//div[@class='ui-pdp-container__row ui-pdp-container__row--main-actions']/form/div/input[2]/@value").get()
        
        precio = response.xpath("//div[@class='ui-pdp-price__second-line']/span[1]/span[1]/text()").get()
        if precio.split(' ')[-1]=='soles':
            precio = float(precio.split(' ')[0] + '.00')
        elif precio.split(' ')[-1]=='céntimos':
            precio = float(precio.split(' ')[0] + '.' + precio.split(' ')[3] + '0')
        else:
            precio = nan
        
        estado = response.xpath("//div[@class='ui-pdp-header']/div/span/text()").get()
        estado = estado.split(" ")[0]

        ubicacion = response.xpath("//div[@class='ui-seller-info__status-info']/div/p[2]/text()").get()

        comentarios = response.xpath("//span[@class='ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--REGULAR ui-pdp-questions__questions-list__question']/text()").getall()
        comentarios = {"{}".format(i):j for i,j in enumerate(comentarios)}

        yield {
            'Titulo': titulo,
            'Link': link,
            'Precio': precio,
            'Estado': estado,
            'Ubicación': ubicacion,
            'Comentarios': comentarios,
            }

'''
Ejecutar en el Terminal/CMD en la ruta que contiene este *py:
CSV: scrapy runspider mercadolibre.py -o mercadolibre.csv
JSON: scrapy runspider mercadolibre.py -o mercadolibre.json
'''

#En el terminal probar (por facilidad) con la siguiente busqueda: ssd nvme blue 
#En el terminal puede que pida ingresar una segunda vez el término de búsqueda: ssd nvme blue

#Seguir probando con más términos de búsqueda: laptop alienware, audifonos, samsung s22, etc...
