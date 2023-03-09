a=0
lgn =0
import time
def fonction_ig() :
    rest_api_key = ""
    rest_identifier = ""
    rest_password = ""

# IG rest login request
    rest_url = "https://demo-api.ig.com/gateway/deal/session"

    headers = {}
    headers["Content-Type"] = "application/json; charset=UTF-8"
    headers["Accept"] = "application/json; charset=UTF-8"
    headers ["Version"] = "2"
    headers ["X-IG-API-KEY"] = rest_api_key

    request_json = {}
    request_json["identifier"] = rest_identifier
    request_json["password"] = rest_password

    rest_response = requests.request("POST", rest_url, headers=headers, json=request_json)
    if rest_response.status_code != 200:
        print("error", rest_response.status_code, rest_url, rest_response.text)
        sys.exit(0)

# collect params from IG rest login response

    xst = rest_response.headers["X-SECURITY-TOKEN"]
    cst	= rest_response.headers["CST"]
    response_json = rest_response.json()
    current_account = response_json["currentAccountId"]
    lightstreamer_endpoint = response_json["lightstreamerEndpoint"]

# IG streaming login request

    streaming_url = "{}/lightstreamer/create_session.txt".format(lightstreamer_endpoint)

    steaming_user = current_account;
    steaming_password = "CST-{}|XST-{}".format(cst, xst)

    query = {}
    query["LS_op2"] = "create"
    query["LS_cid"] = "mgQkwtwdysogQz2BJ4Ji kOj2Bg"
    query["LS_user"] = steaming_user
    query["LS_password"] = steaming_password

    streaming_response = requests.request("POST", streaming_url, data=query, stream=True)
    if streaming_response.status_code != 200:
        print("error", streaming_response.status_code, streaming_url, streaming_response.text)
        sys.exit(0)
    else:
        print("ok")
# collect params from streaming response opérationneljusqu'ici
    streaming_iterator = streaming_response.iter_lines(chunk_size=8, decode_unicode=True)

    
    
    n=0
    for line in streaming_iterator:
        print(line)
        n=n+1
        liste=line.split(':')
        for i in range(len(liste)):
            if liste[i]=="ControlAddress":
                control_domain = liste[i+1]
            if liste[i] == "SessionId":
                streaming_session = liste[i+1] 
        if n>5 :break 
        
    
    
  
    control_url = "https://{}/lightstreamer/control.txt".format(control_domain)

    query = {}
    query["LS_session"] = streaming_session
    query["LS_op"]="add"
    query["LS_table"]="1"
#query["LS_id"]="MARKET:CS.D.EURUSD.MINI.IP" et IX.D.CAC.IDF.IP IX.D.DOW.(DAILY).IP
    query["LS_id"]="L1:CS.D.GBPUSD.CFD.IP L1:CS.D.EURUSD.CFD.IP L1:CS.D.BITCOIN.CFD.IP L1:IX.D.CAC.IDF.IP  L1:IX.D.DOW.IDF.IP  L1:IX.D.DAX.IDF.IP L1:CS.D.USDJPY.CFD.IP L1:CS.D.AUDUSD.CFD.IP L1:CS.D.GBPEUR.CFD.IP L1:CS.D.EURCHF.CFD.IP L1:CC.D.LCO.UME.IP" #operationnel
#query["LS_id"]="CHART:CS.D.BITCOIN.CFD.IP:1MINUTE"
#query["LS_schema"]="BID OFFER"
    query["LS_schema"]="BID OFFER "
    query["LS_mode"]="MERGE"

    control_response = requests.request("POST", control_url, data=query)
    if control_response.status_code != 200:
        print("error", control_response.status_code, control_url, control_response.text)
        sys.exit(0)

# stream prices

    for line in streaming_iterator:
        print(line)
        #out[lgn] = line.split("|")
        lgn+=1
        
        
        
        
while a !=6: 
    try:
        fonction_ig()
    except:
        #print(out)
        time.sleep(60)
        pass