from constants import *
from bs4 import BeautifulSoup
import requests
import lxml
from dataclasses import dataclass, asdict
import unicodedata
import time

@dataclass
class car:
    id: int
    marque: str
    modele: str
    generation: str | None
    carrosserie: str
    couleur_exterieure: str
    couleur_interior: str
    sellerie: str
    nombre_de_places: int
    nombre_de_portes: int
    moteur: str
    puissance: str
    energie: str
    boite_vitesse: str
    puissance_fiscale: str
    transmission: str
    cylindree: str | None
    kilometrage: str
    mise_en_circulation: str | None
    etat_general: str | None
    anciens_proprietaires: int | None
    prix: int

def get_page_source_code(url, **kwargs):
    if kwargs.get("page"):
        html_text = requests.get(url+"/"+str(kwargs.get("page"))).text
    else:
        html_text = requests.get(url).text
    soup = BeautifulSoup(html_text,"lxml")
    return soup

def get_sale_offers(soup):
    cars_urls = [car["href"].replace("/fr/occasion/","") for car in soup.find_all("a",class_="occasion-link-overlay")]
    return cars_urls

def remove_accents(text):
    # Normalize to NFKD form, which separates characters from their accents
    nfkd_form = unicodedata.normalize('NFKD', text.lower())
    # Filter out combining characters (i.e., accents)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)]).strip()


def get_specifications(soup):
    car_dict = {}
    # list of required fields for specification
    required_data = ["Marque",
                     "Modèle",
                     "Génération",
                     "Carrosserie",
                     "Couleur extérieure",
                     "Couleur intérieure",
                     "Sellerie",
                     "Nombre de places",
                     "Nombre de portes",
                     "Moteur",
                     "Puissance",
                     "Énergie",
                     "Boite vitesse",
                     "Puissance fiscale",
                     "Transmission",
                     "Cylindrée",
                     "Kilométrage",
                     "Mise en circulation",
                     "État général",
                     "Anciens propriétaires"]
    
    required_tag_classes = ["col-md-6 mb-3 mb-md-0","col-md-6","box d-none d-md-block"]

    # get the id for the car sale
    breadcrumps = soup.find("ul", class_="breadcrumbs")
    id = breadcrumps.find("li",class_="active").text.replace("#","")
    car_dict["id"] = id

    # pre-fill car_dict required fields
    for field in required_data:
        car_dict[remove_accents(field).replace(" ","_")] = ""
    
    for tag_class in required_tag_classes:
        if tag_class == required_tag_classes[2]:
            data = soup.find("div",class_=tag_class)

            # get car price
            car_dict["prix"] = ",".join(data.find("div",class_= "price" ).text.strip().split()).replace(",DT"," DT")

            # get additional general info
            specs = data.find_all("li")
            for spec in specs:
                details = spec.find_all("span")

                label = details[0].text.strip()
                value = details[1].text.strip()

                if label in required_data:
                    if label == "Kilométrage":
                        car_dict[remove_accents(label).replace(" ","_")] = ",".join(value.split()).replace(",km"," km")
                    elif label == "Puissance fiscale":
                        car_dict[remove_accents(label).replace(" ","_")] = " ".join(value.split())
                    else:
                        car_dict[remove_accents(label).replace(" ","_")] = remove_accents(value)

        else:

            for div in soup.find_all("div", class_= tag_class):
                if ' '.join(div["class"]).strip() == tag_class:
                    specifications = div.find_all("li")
                    for specification in specifications:
                        details = specification.find_all("span")
                        car_dict[remove_accents(details[0].text).replace(" ","_")] = details[1].text.replace(" ","")
    return car_dict
                

def parse_car_info(soup):
    # get car model_specification like brand, modele, chassis name etc 
    car_specifications = get_specifications(soup)

    
    new_car = car(
        id= car_specifications["id"],
        marque= car_specifications["marque"],
        modele= car_specifications["modele"],
        generation= car_specifications["generation"],
        carrosserie= car_specifications["carrosserie"],
        couleur_exterieure= car_specifications["couleur_exterieure"],
        couleur_interior= car_specifications["couleur_interieure"],
        sellerie= car_specifications["sellerie"],
        nombre_de_places= car_specifications["nombre_de_places"],
        nombre_de_portes= car_specifications["nombre_de_portes"],

        moteur= car_specifications["moteur"],
        puissance= car_specifications["puissance"],
        energie= car_specifications["energie"],
        boite_vitesse= car_specifications["boite_vitesse"],
        puissance_fiscale= car_specifications["puissance_fiscale"],
        transmission= car_specifications["transmission"],
        cylindree= car_specifications["cylindree"],

        kilometrage= car_specifications["kilometrage"],
        mise_en_circulation= car_specifications["mise_en_circulation"],
        etat_general= car_specifications["etat_general"],
        anciens_proprietaires= car_specifications["anciens_proprietaires"],
        prix= car_specifications["prix"]

    )

    return new_car


if __name__ == "__main__":
    cars = []
    soup = get_page_source_code(URL)
    cars_url = get_sale_offers(soup)
    # print(cars_url)
    car_soup = get_page_source_code(TEST_CAR)
    print(parse_car_info(car_soup))

    # for url in cars_url:
    #     car_soup = get_page_source_code(url)
    #     car_sale = parse_car_info(car_soup)
    #     print(car_sale)
    #     if car_sale is not None:
    #         cars.append(asdict(car_sale))
    #         time.sleep(0.5)
    # print(cars)
            

