from constants import *
from bs4 import BeautifulSoup
import requests
import lxml
from dataclasses import dataclass, asdict, fields
import unicodedata
import time
import random
import csv
import argparse
import re
import os

@dataclass
class Car:
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

def get_page_source_code(url,**kwargs):
    if kwargs.get("page"):
        print(url + str(kwargs.get("page")))
        response = requests.get(url + str(kwargs.get("page")),headers=HEADERS).text
    else:
        response = requests.get(url,headers=HEADERS).text
    soup = BeautifulSoup(response,"lxml")
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
                    elif label == "Mise en circulation":
                        car_dict[remove_accents(label).replace(" ","_")] = value.replace(".","-")
                    else:
                        car_dict[remove_accents(label).replace(" ","_")] = remove_accents(value)

        else:

            for div in soup.find_all("div", class_= tag_class):
                if ' '.join(div["class"]).strip() == tag_class:
                    specifications = div.find_all("li")
                    for specification in specifications:
                        details = specification.find_all("span")
                        car_dict[remove_accents(details[0].text).replace(" ","_")] = " ".join(details[1].text.split()).strip()
    return car_dict
                

def parse_car_info(soup):
    # get car model_specification like brand, modele, chassis name etc 
    car_specifications = get_specifications(soup)

    
    new_car = Car(
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

def get_next_page(soup):
    paginator = soup.find("ul", class_="pagination")
    #print(paginator)
    if not paginator.select_one("li.page-item.next.disabled"): 
        return re.sub(r".*/", "", paginator.select_one("li.page-item.next").find("a").get("href")) #.replace("/fr/occasion/","").replace("s=brand%21%3Avolkswagen/","")
    else:
        return 
        
def append_to_csv(car,marque=""):
    file_name = f"outputs/cars.csv"
    if marque:
        file_name = f"outputs/cars_{marque}.csv"
    
    file_exists = os.path.isfile(file_name)

    fields_names = [field.name for field in fields(Car)]
    with open(file_name,"a", encoding= "utf-8") as f:
        writer = csv.DictWriter(f,fieldnames=fields_names)
        if not file_exists:
            writer.writeheader()
        writer.writerow(car)
        print("successfully added data to CSV file")

def main(marque=None):
    
    url = URL
    
    if marque:
        url += f"s=brand!:{marque.lower()}/"
        print(url)

    # create a variable delay between requests
    delay = random.uniform(2, 10)  # 2 to 10 seconds

    # count the number of web pages that will be scrapped
    num_pages = 0
    
    #set the first page for scarpping
    homepage = url
    current_page = 1

    while True:
        soup = get_page_source_code(homepage, page = current_page)
        cars_url = get_sale_offers(soup)
        
        print(cars_url)

        for url in cars_url:
            print(homepage + url)
            car_soup = get_page_source_code(homepage + url)
            car_sale = parse_car_info(car_soup)

            print(car_sale)

            if car_sale is not None:
                append_to_csv(asdict(car_sale),marque)
                time.sleep(delay)

        # get next page url
        current_page = get_next_page(soup)
        print(current_page)
        num_pages += 1

        if not current_page: 
            break
    

def test():
    car_soup = get_page_source_code(TEST_CAR2)
    car_sale = parse_car_info(car_soup)
    print(car_sale)
    
def test_next_page():
    soup = get_page_source_code(URL)
    print(get_next_page(soup))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Car scraper with optional marque filter.")
    parser.add_argument("--marque", type=str, help="Brand filter for car scraping (e.g., 'Toyota')")
    args = parser.parse_args()

    main(marque=args.marque)
    
    # test()
    # test_next_page()

    
            

