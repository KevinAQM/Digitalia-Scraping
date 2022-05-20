import scrapy
from scrapy_splash import SplashRequest
from numpy import nan
import pandas as pd 

class VealaptopSpider(scrapy.Spider):
    name = 'vealaptop'

    file = pd.read_csv("links.csv")
    links =list(file['links'])
    
    def start_requests(self):                                                   
        for url in self.links:                                              
            yield SplashRequest(url=url, callback=self.parse_products)

    def parse_products(self,response):

        titulo = response.xpath("//div[@class='ProductCard__wrapper']/div[2]/h6/div/text()").get()
        link = response.url
        
        #marca
        marca = response.xpath("//div[@class='ProductCard__information__productdata__name']/span/div/a/text()").get()
        
        #modelo
        try:
            modelo = response.css(".Modelo::text").get()
        except:
            modelo = None

        # # tarjeta de video
        # tarjeta_de_video = response.css(".Tarjeta-de-Video::text").getall()

        # # procesador  computo
        # procesador_de_video = response.css(".Procesador-Computo::text").getall()

        # # ram
        # ram = response.css(".Memoria-RAM::text").getall()

        #entrada usb
        # cant_entrada_usb = response.css(".Entradas-USB::text").getall()

        # # entrada hdmi
        # hdmi = response.css(".Entradas-HDMI::text").getall()

        # # tamaño de pantalla
        # pantalla = response.css(".Pantalla-Computo-Pulgadas-::text").getall()

        # # tipo de disco
        # tipo_disco = response.css(".Tipo-De-Disco-Duro::text").getall()

        # # disco duro
        # disco_duro = response.css(".Capacidad-De-Disco-Duro::text").getall()

        # # disco solido
        # disco_solido = response.css(".Disco-Duro-Solido::text").getall()

        # #camara
        # camara = response.css(".Camara::text").getall()

        yield{
            'titulo': titulo,
            'link': link,
            #'precio_normal': precio_normal,
            #'precio_internet': precio_internet,
            #'precio_tarjeta_oh': precio_tarjeta_oh,
            'modelo': modelo,
            'marca': marca,
            # 'tarjeta_de_video': tarjeta_de_video,
            # 'procesador_de_video': procesador_de_video,
            # 'ram': ram,
            # 'cant_entrada_usb': cant_entrada_usb,
            # 'hdmi': hdmi,
            # 'pantalla': pantalla,
            # 'tipo_disco': tipo_disco,
            # 'disco_duro': disco_duro,
            # 'disco_solido': disco_solido,
            # 'camara': camara,
        }

# scrapy runspider vealaptop.py -o vealaptop.csv