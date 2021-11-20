from flask import Flask,render_template,request,jsonify
from websocket import create_connection
from flask_mysqldb import MySQL
import yaml
app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MySQL_HOST']= db['mysql_host']
app.config['MySQL_USER']= db['mysql_user']
app.config['MySQL_PASSWORD'] = db['mysql_password']
app.config['MySQL_DB'] = db['mysql_db']
mysql = MySQL(app)
data = []
value = []
@app.route('/')



def hello_world():
    
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
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users(labels,value) VALUES(%s %s)", (labels , value))
    mysql.connection.commit()
    cur.close()

    return render_template('graph.html',labels=labels,values=value)

if __name__ == "__main__":
    app.run(debug=True)
