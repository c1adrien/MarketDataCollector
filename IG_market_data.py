# Getting IG Market data 
import requests

head = {"Content-Type":"application/json; charset=UTF-8",
        "Accept":"application/json; charset=UTF-8",
        "VERSION":"2",
        "X-IG-API-KEY":""}

playloads = {"identifier":"",
            "password":""}


# CST and X_SECURITY_TOKEN 


import json

r = requests.post("https://demo-api.ig.com/gateway/deal/session",headers=head,data=json.dumps(playloads))

CST = r.headers['CST']
X_SECURITY_TOKEN = r.headers['X-SECURITY-TOKEN']


#We will now simply ask for the market sentiment using a query, for example. We want to use CST and X_SECURITY_TOKEN. Note that we are switching to a GET request.

head = {"Content-Type":"application/json; charset=UTF-8",
        "Accept":"application/json; charset=UTF-8",
        "X-IG-API-KEY":"",
        "CST":CST,
        "X-SECURITY-TOKEN":X_SECURITY_TOKEN}

r = requests.get("https://demo-api.ig.com/gateway/deal/clientsentiment/EURUSD", headers=head)
json.loads(r.text) 


r = requests.get("https://demo-api.ig.com/gateway/deal/markets?searchTerm=eur",headers=head)
json.loads(r.text) 


url = "https://demo-api.ig.com/gateway/deal/prices/"
url += "CS.D.sp_EURRUB.CFD.IP/"
url+= "MINUTE_5"
url+= "?startdate="
url+="2021:03:15-15:00:00"
url+="&enddate="
url+= "2021:03:19-12:00:00"

r = requests.get(url,headers=head)

r.text

#make an acceptable format

import json
commit_data = json.loads(r.text) 
commit_data.keys()

commit_data['prices'] #on



df = pd.json_normalize(commit_data['prices'])
print(df)


plt.figure(figsize=(20,10))
df['openPrice.bid'].plot()
