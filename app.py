from flask import Flask,render_template,request,jsonify
from websocket import create_connection
import time

import pickle
looperCPU = 500
start = time.time()
app = Flask(__name__)

data = []
value = []
@app.route('/')

def hello_world():
    while(looperCPU != 0):
        time.sleep(60)
        ws = create_connection("wss://fx-ws-testnet.gateio.ws/v4/ws/btc")
        ws.send('{"time" : 123456, "channel" : "futures.candlesticks", "event": "subscribe", "payload" : ["1m", "BTC_USD"]}')
        print(ws.recv())
        data.append(ws.recv())
        labels = [row[0] for row in data]
        value.append(
            [row[1] for row in data],
            [row[2] for row in data],
            [row[3] for row in data]
        )
        

    return render_template('graph.html',labels=labels,values=value)
'''
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/predict',methods=['POST'])
def predict():
  if request.method == "POST" :

     Loss = int(request.form["Loss"])
     dis = int(request.form["dis"]) 
     Fever = int(request.form["Fever"])
     Bp = int(request.form["Bp"])
     st = int(request.form["st"])

     
     with open('mod','rb') as f:
         model = pickle.load(f)    
     result = model.predict([[Loss, dis, Fever, Bp, st]])
     if result[0] == "covid-19":
       return render_template('index.html',data=["You have covid-19 symptoms consult doctor"])  
     else:
        return render_template('index.html',data=["You have Malaria symptoms consult doctor"])    

'''
if __name__ == "__main__":
    app.run(debug=True)
