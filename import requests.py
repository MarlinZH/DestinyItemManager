import requests
import json
import pandas as pd
import pyodbc

#Connect to Database
#Variable Value Assignement
API_KEY = 'ba7c2864c8bf4a9fb53266c76f6d6777'
USER_AGENT = ''
payload = {
    'api_key'= API_KEY
}
#Methods

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)




#Request

response = requests.get("http://api.open-notify.org/astros.json")#Naked Request
response = requests.get("",params = parameters)#Header and Paramater Request

# Outputs
print(response.status_code)
jprint(response.json())
#Connect to Destiny 2 API

#Pull in Current Player inventory
#Pull all Destiny 2 Items
#Create Data Structures
