import scrapy
from scrapy_splash import SplashRequest
from numpy import nan

class RipleySpider(scrapy.Spider):
    name = "ripley"
    
    def start_requests(self):
        url = 'https://simple.ripley.com.pe/tecnologia/computacion/laptops?facet%5B%5D=Procesador%3AIntel+Core+i7'
        yield SplashRequest(url)

    def parse(self, response):
        for link in response.xpath("//div[@class='catalog-container']/div/a/@href"):
            yield response.follow(link.get(), callback=self.parse_products)

    def parse_products(self, response):
        titulo = response.css("h1::text").get()
        link = response.request.url
        sku = response.css(".sku-value::text").get()

        precio = response.css(".product-price::text").getall()
        if len(precio)==1: 
            precio_normal = nan
            precio_internet = precio[0]
            precio_tarjeta_ripley = nan
        elif len(precio)==2:
            precio_normal = precio[0]
            precio_internet = precio[1]
            precio_tarjeta_ripley = nan
        elif len(precio)==4:
            precio_normal = precio[0]
            precio_internet = precio[1]
            precio_tarjeta_ripley = precio[-1]

        descripcion = response.css(".product-short-description::text").get()

        yield {
            'Título': titulo,
            'Link': link,
            'SKU': sku,
            'Precio Normal': precio_normal,
            'Precio Internet': precio_internet,
            'Precio Tarjeta Ripley': precio_tarjeta_ripley,
            'Descripción': descripcion,
        }
        

'''
Ejecutar en el Terminal/CMD en la ruta que contiene este archivo ripley.py:
Salida en formato CSV: scrapy runspider ripley.py -o ripley.csv
Salida en formato JSON: scrapy runspider ripley.py -o ripley.json

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
