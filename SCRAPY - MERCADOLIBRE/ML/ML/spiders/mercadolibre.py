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

        puntuacion = response.xpath("//p[@class='ui-review-view__rating__summary__average']/text()").get()
        # puntuacion = response.css(".ui-review-view__rating__summary__average::text").extract()
        ubicacion = response.xpath("//div[@class='ui-seller-info__status-info']/div/p[2]/text()").get()

        comentarios = response.css(".ui-pdp-questions__questions-list__question::text").getall()
        comentarios = {"{}".format(i):j for i,j in enumerate(comentarios)}

        yield {
            'Titulo': titulo,
            'Link': link,
            'Precio': precio,
            'Estado': estado,
            'Puntuación': puntuacion,            
            'Ubicación': ubicacion,
            'Comentarios': comentarios,
            }

'''
Ejecutar en el Terminal/CMD en la ruta que contiene este archivo mercadolibre.py:
Salida en formato CSV: scrapy runspider mercadolibre.py -o mercadolibre.csv
Salida en formato JSON: scrapy runspider mercadolibre.py -o mercadolibre.json

#En el terminal probar (por facilidad) con la siguiente busqueda: ssd nvme blue 
#En el terminal puede que pida ingresar una segunda vez el término de búsqueda: ssd nvme blue
#Seguir probando con más términos de búsqueda: laptop alienware, audifonos, samsung s22, etc...
'''

'''
Para probar cada comando (y su respuesta) usar en el Terminal/CMD:
1. scrapy shell
2. from scrapy import Request
3. req = Request(url ='your-link', headers = {your-headers})
4. fetch(req)
5. Probar código paso a paso: response.xpath("yourxpath").get()

Para el paso 3. usar estos headers↓↓↓
{"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"sec-fetch-site":"cross-site","sec-fetch-mode":"navigate","sec-fetch-user":"?1","sec-fetch-dest":"document","referer":"https://pipedream.com/@kevinaqm/requestbin-p_6lCL75w/inspect",
"accept-encoding":"gzip, deflate, br","accept-language":"es-PE,es-419;q=0.9,es;q=0.8,en;q=0.7"}

'''