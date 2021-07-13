# Brutus_DataVisualization
 
#### For at programmet skal fungere må [python3](https://www.python.org/downloads/)  være installert.
 
#### Det er også en fordel å installere [pip](https://www.geeksforgeeks.org/how-to-install-pip-on-windows/)!
 
__Følgende biblioteker må installeres for at programmet skal fungere. Bibliotekene kan installeres ved å lime inn teksten under i terminalen.__
 
* pip3 install dash
* pip3 install PyMySql
* pip3 install dash_bootstrap_components
* pip3 install pandas
* pip3 install sqlalchemy
* pip3 install pyodbc

.
Applikasjon er bygget ved hjelp av Dash Plotly, et rammeverk som muliggjør presentasjon 
data i form av enkle applikasjoner. Applikasjonen er skrevet i Python, og er bygget opp slik:

.
dash_visualization 
├── dash_visualization # Source files
└── README.md		# Readme file

.
├── ...
├── apps                   	# apps/pages of the application
│   ├── app1.py        	# Table page
│   ├── app2.py        	# Map page
│   ├── app3.py        	# Load data page
│   └── app4.py        	# Graph page
├── index.py			# App navigation
├── app.py			# Dash app configuration
├── static                   	# static files
│   ├── custom.css      # Graphic appearance configuration file
│   ├── datasett.csv    	# .csv file with user data

 