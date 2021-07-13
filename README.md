# Brutus A/S

## Hvordan brukes applikasjonen?
Applikasjonen er delt opp i fire sider
* Tabell
Her vil brukeren få muligheten til å filtrere data ut i fra stedsinformasjon, aldersspenn og fritekst. Resultatet blir presentert i en tabell.

* Graf
Denne siden inneholder en graf som visualiserer aldersfordelingen blant brukerne. Her er det også mulig å filtere på stater, for å få en mer detaljert presentasjon.
* Kart
Her får man muligheten til å se fordelingen av antall brukere utover alle de amerikanske statene, presentert i et koropletkart. En nedtrekksmeny gir også muligheten for å se hva som er gjennomsnittsalderen på brukerne fra hver enkelt stat.
* Last opp fil
På denne siden kan man laste opp .csv eller .xls filer med brukerdata. Man får også muligheten til å laste ned brukerdata fra en MySQL-server, samt laste opp brukerdata til samme server. Merk at ved å laste opp, vil gammel data bli erstattet.
Server-funksjonaliteten er for øyeblikket utilgjengelig uten VPN-tilkobling, som et sikkerhetsmessig tiltak.

## Hva løser applikasjonen?
Applikasjonen muliggjør rask visualisering av data, ved å presentere data i en dynamisk tabell med en rekke ulike filtreringsmuligheter. Applikasjonen gir deg også mulighet til å enkelt identifisere trender på tvers av datamengdene ved å visualisere den både i en graf og i et kart. 

## Hvordan kjører jeg programmet?
#### For at programmet skal fungere må [python3](https://www.python.org/downloads/)  være installert.
 
#### Det er også en fordel å installere [pip](https://www.geeksforgeeks.org/how-to-install-pip-on-windows/)!
 
__Følgende biblioteker må installeres for at programmet skal fungere. Bibliotekene kan installeres ved å lime inn teksten under i terminalen.__
 
* pip3 install dash
* pip3 install PyMySql
* pip3 install dash_bootstrap_components
* pip3 install pandas
* pip3 install sqlalchemy
* pip3 install pyodbc

Når dette er gjort, er det bare å kjøre filen **index.py**, ved å skrive **python3 index.py** i terminalen, eller ved å bruke en valgfri IDE.
Deretter vil appen være tilgjengelig ved å gå inn på denne linken i nettleseren:
* [http://127.0.0.1:8050/apps](http://127.0.0.1:8050/apps) 

## Hvordan er applikasjonen bygget?
Applikasjon er bygget ved hjelp av [Dash Plotly](https://plotly.com/dash//), et rammeverk som muliggjør presentasjon 
data i form av enkle applikasjoner. Applikasjonen er skrevet i Python, og er bygget opp slik:

    ├── dash_visualization 			# Source files
    └── README.md				# Readme file

    ├── apps                   		# apps/pages of the application
    │   ├── app1.py        			# Table page
    │   ├── app2.py        			# Map page
    │   ├── app3.py        			# Load data page
    │   └── app4.py        			# Graph page
    ├── index.py				# App navigation
    ├── app.py				# Dash app configuration
    ├── static                   		# static files
    │   ├── custom.css      		# Graphic appearance configuration file
    │   ├── datasett.csv    		# .csv file with user data
    
    
    