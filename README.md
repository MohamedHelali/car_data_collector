# Car data Collector

## About the project
This script automates the collection of car sales listings from the Tunisian website [automobile.tn](https://www.automobile.tn) and saves
the extracted data into a CSV file.
It was developed as part of an effort to gather a large, structured dataset for analyzing the used car market in Tunisia.
The ultimate goal is to use this data to better understand pricing trends and, if possible, build a predictive models that
estimates used car cales based on current market conditions.

## project structure
 * **outputs**: Directory where the scraped car listings are saved as CSV files.
 * **last_page.txt**: Tracks the last successfully scraped page (used for resume functionality).
 * **main.py**: Main script containing the scraping and data processing logic.
 * **constants.py**: Stores all constants used across the script (e.g., URLs, headers).
 * **requirements.txt**: Lists all required Python libraries for the project.

## Installing Libraries

The **requirements.txt** file  contains all the libraries used in this application.
 These libraries can be  easily installed using the following pip command:
 ```console
 pip install -r requirements.txt
```

## Usage
To run the script, simply execute the **main.py** file:
```console
python main.py
```
### Optional: Filter By Car Brand:
You can target listings for a specific car brand (e.g., Mercedes, BMW, etc.) using the `--marque`
argument:
```console
python main.py --marque mercedes
```
This will instruct the sccraper to collect only car sale listings related to the specified brand.

## Example Output
After execution, the script generates a CSV file containing car sale listings. Each row in the file
represents a single car listing, and the columns contain key details such as:

|id |marque|modele|generation|carrosserie|couleur_exterieure|couleur_interior|sellerie|nombre_de_places|nombre_de_portes|moteur|puissance|energie|boite_vitesse|puissance_fiscale|transmission|cylindree|kilometrage|mise_en_circulation|etat_general|anciens_proprietaires|prix|
|-----|-------------|-------------------------------------------|----------|-----------|------------------|----------------|--------|----------------|----------------|------|---------|-------|-------------|-----------------|------------|---------|-----------|-------------------|------------|---------------------|----|
110337|mercedes benz|classe c|(206) berline03/2021   aujourd'hui|berline|bleu|noir|similicuir|5|4|180 1.5 i 16v eq boost 9g tronic||hybride leger essence|automatique|10 cv|propulsion|1496 cm3|36,000 km|07-2021|tres bon|1ere main|206,000 DT
113928|mahindra     |kuv 100|01/2016   aujourd'hui|suv|blanc|gris|tissu|5|4|1.2 82cv|82 ch dyn|essence|manuelle|5 cv|traction|1200 cm3|60,000 km|09-2021|tres bon|1ere main|33,000 DT

For a better understanding of the CSV structure, here is a breakdown of each column and its meaning:

| Column Name             | Description                                                        |
| ----------------------- | ------------------------------------------------------------------ |
| `id`                    | Unique identifier for the listing (if provided by the website).    |
| `marque`                | Car brand (e.g., Volkswagen, Mercedes, BMW).                       |
| `modele`                | Car model name (e.g., Golf, C-Class, 208).                         |
| `generation`            | Specific generation/version of the model (if available).           |
| `carrosserie`           | Body type (e.g., Berline, SUV, Hatchback).                         |
| `couleur_exterieure`    | Exterior color of the vehicle.                                     |
| `couleur_interior`      | Interior color of the vehicle.                                     |
| `sellerie`              | Type of upholstery (e.g., cuir = leather, tissu = fabric).         |
| `nombre_de_places`      | Number of seats in the car.                                        |
| `nombre_de_portes`      | Number of doors.                                                   |
| `moteur`                | Engine name or code (as listed).                                   |
| `puissance`             | Engine power (e.g., 110 ps).                                       |
| `energie`               | Fuel type (e.g., essence = petrol, diesel, électrique = electric). |
| `boite_vitesse`         | Transmission type (e.g., manuelle = manual transmission, automatique = automatic).                   |
| `puissance_fiscale`     | Fiscal horsepower (used for registration/tax purposes in Tunisia). |
| `transmission`          | Drivetrain type (e.g., traction, propulsion, intégrale = AWD).     |
| `cylindree`             | Engine displacement in cm³ (e.g., 1598).                           |
| `kilometrage`           | Total mileage of the vehicle in kilometers.                        |
| `mise_en_circulation`   | Date of first registration (format: MM.YYYY).                      |
| `etat_general`          | General condition of the car (e.g., Très bon = very good, Bon état = good condition , Moyen = Average condition).    |
| `anciens_proprietaires` | Number of previous owners (e.g., 1ère main = first owner).         |
| `prix`                  | Listed price in Tunisian Dinar (DT).                               |

> [!NOTE]
> Some listings may not provide all values. Missing information will appear as blank fields in the CSV file.

The output is saved in the `outputs/` folder inside a csv file named `cars.csv`. if a specific
brand is specified using `--marque` argument, the file will be saved under a name that includes the brand 
(e.g., `cars_mercedes.csv`)

## Resume Functionality
To make the scraping process more robust, the script includes a resume mechanism in case it is interrupted (e.g., due to network failure or manual stop).
* the `last_page_txt` file keeps track of the last successfully scraped page.
* if the script is restarted, it will automatically continue from the next unprocessed page.
* this ensures that no previously collected data is lost or reprocessed.

> [!NOTE]
> if `last_page.txt` does not exist or is empty, the script will start from page 1.

## Author: Mohamed Helali

