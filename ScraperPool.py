import requests
from bs4 import BeautifulSoup 
from calendar import monthrange
import time
import pickle
from multiprocessing import Pool

#SETTINGS

MONTHS = ["Gennaio","Febbraio","Marzo","Aprile","Maggio","Giugno","Luglio","Agosto","Settembre","Ottobre","Novembre","Dicembre"]
TRESHOLD_DAYS = 15
TRESHOLD_MONTHS = 3
CITIES_TO_SCRAPE = ['Cologno+Monzese','Sora', 'Pescara', 'Calcinaia', 'Castelvetrano', 'Cismon+Del+Grappa', 'Cavallermaggiore', 'Lograto', 'Cassano+Magnago', 'Bondeno', 'Vercelli', 'Mercato+San+Severino', 'Venetico+Marina', 'Fombio', 'Acquasparta', 'Codevigo', 'Cremona', 'Forli', 'Cento', 'Orsago', 'Tortona', 'Ravenna', 'Bologna', 'Poggibonsi', 'Ramacca', 'Venezia', 'Oleggio', 'S.agata+Li+Battiati', 'Montesarchio', 'Formia', 'Marigliano', 'Lucca', 'Catanzaro', 'Viareggio', 'Pisa', 'Portogruaro', 'Ragusa', 'Capaccio', 'Lumezzane', 'Enna', 'San+Cesario+Di+Lecce', 'Frosinone', 'Brescello', 'Acerra', 'Reggio+Calabria', 'Galatone', 'Rezzato', 'Lendinara', 'Vibo+Valentia', 'Arzano', 'Spoleto', 'Vicenza', 'Castellanza', 'Vigliano+Biellese', 'Mandello+Del+Lario', 'Nizza+Monferrato', 'Napoli', 'Camisano+Vicentino', 'Pistoia', 'Cittaducale', 'Salzano', 'Ancona', 'Rovigo', 'Macchia+Di+Isernia', 'Perugia', 'Taglio+Di+Po', 'Montecchio+Maggiore', 'Foligno', 'Scandicci', 'Torino', 'Padova', 'Castrocaro+Terme', 'Serramazzoni', 'Sanremo', 'Acireale', 'Reggio+Emilia', 'Squinzano', 'Acquaviva+Delle+Fonti', 'Collepasso', 'Siracusa', 'Genova', 'Monza', 'Prato', 'Udine', 'Arezzo', 'Giarre', 'Mentana', 'Senigallia', 'Forlimpopoli', 'Verona', 'Imola', 'Lamezia+Terme', 'Martellago', 'Badia+Polesine', 'Rimini', 'Revello', 'Vezzano+Ligure', 'Acqui+Terme', 'Torre+Del+Greco', 'Airola', 'Camponogara', 'Moncalvo', 'Palermo', 'Tolentino', 'Bari', 'Pesaro', "Pomigliano+D'arco", "Fiorenzuola+D'arda", 'Cesena', 'Casalgrande', 'Latina', 'Chioggia', 'Valenza', 'Medicina', 'Sandigliano', 'Ivrea', "Arqua'+Polesine", 'Agro+Di+Salandra', 'Brescia', 'Novara', 'Mongrando', 'Briatico', 'Gela', 'Mistretta', 'Pontevico', 'Revere', 'Vergiate', 'Rosarno', 'Sergnano', 'Modena', 'Cavriago', 'Isola+Del+Liri', 'Binetto', 'Cavarzere', 'Afragola', 'Sovizzo', 'San+Benedetto+Del+Tronto', 'Amelia', 'Mantova', 'Belpasso', 'Firenze']
    
#CITIES_TO_SCRAPE = ['Sora']
NUM_OF_MONTHS = 12
YEAR_TEXT = "2018"
YEAR_INT = int(YEAR_TEXT)
NUM_OF_THREADS = 7
STORE_LOAD_PRINT = (True,False,False) 


def scrape_city(city): 

    startTime = time.time()

    data={}

    data[city]={}
    print("#################################################################################")
    print(city + " STARTING..... ")
    
    url = "https://www.ilmeteo.it/portale/archivio-meteo/{0}/".format(city)     

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml') 

  
    table = soup.find_all('td', text=YEAR_TEXT)
    if(len(table))<1: #city doesn't exist -> drop it
        print("Missing city on: " + url)
        diz[city]="n/a"
        return data  
 

    missing_months = 0  
    index_month = 0
    while(index_month < NUM_OF_MONTHS and missing_months<TRESHOLD_MONTHS): 
            
            data[city][index_month+1]={}
           

            day_in_month = monthrange(YEAR_INT, index_month+1)[1] 

           
            
            missing_days = 0            
            for day in range(1,day_in_month+1): #loop over each day of month
               
                url = "https://www.ilmeteo.it/portale/archivio-meteo/{2}/{3}/{1}/{0}".format(day,MONTHS[index_month],city,YEAR_TEXT)
               
                r = requests.get(url)
                
                soup = BeautifulSoup(r.text, 'html.parser')
                
                table = soup.find_all('table')
                
                data[city][index_month+1][day]={}

                if(len(table)<4): #day missing
                    print("Missing Values on URL: " + url)
                    data[city][index_month+1][day]="n/a"
                    missing_days += 1
                    continue  #go to the next day
                  
                else: 
                
                    info_day = table[3].find_all('td')  #get data
                    
                
                for i in range(len(info_day)):   #loop over info and store into dict properly
                
                    if(i%2==0): 
                        label=info_day[i].text
                    else: 
                        data[city][index_month+1][day][label]=info_day[i].text
            
            if missing_days>TRESHOLD_DAYS: #if there are too many missing day take note of it
                missing_months +=1 
                print("TRESHOLD EXECEEDED " + city + " Valore: " + str(missing_months))

            print("Month " + MONTHS[index_month] + " Completed" + "........" + city)

            index_month+=1

    endTime = time.time()
    print(city + " END SCRAPING " + " DURATION " +  str(endTime-startTime))
    if(missing_months>=TRESHOLD_MONTHS): 
        print(city + " END SCRAPING " + " DURATION " +  str(endTime-startTime) + " MONTH TRESHOLD REACHED ")
        data = {}
        data[city]="n/a"
    print("#################################################################################")
    print()

    return data
        



def store_diz(data): 



    with open("mySavedDict.txt", "wb") as myFile:
        pickle.dump(data, myFile)

def pull_diz(): 

    with open("mySavedDict.txt", "rb") as myFile:
        myNewPulledInDictionary = pickle.load(myFile)

    return myNewPulledInDictionary






if __name__ == '__main__':



    with Pool(NUM_OF_THREADS) as p: #increase throughput
        diz = p.map(scrape_city, CITIES_TO_SCRAPE)
    


    store = STORE_LOAD_PRINT[0]
    load = STORE_LOAD_PRINT[1]
    show = STORE_LOAD_PRINT[2]
    

    if store: 
        store_data(data)
    if load: 
        data = load_data()
    if show: 
        print(data)






