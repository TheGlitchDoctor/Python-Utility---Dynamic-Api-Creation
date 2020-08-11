
from psutil import process_iter
from signal import SIGTERM # or SIGKILL
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_socketio import SocketIO, send, emit
from functions_lookup import functions_lookup
import inspect, ast
#import subprocess
import os


#?Main server
app=Flask(__name__, template_folder='template')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

#?Data for all connected users and running/halted servers
users=0
buffer_ports=[]
active_ports={}
tableData=[]

#?Loads table data when user clicks on Use Service
def loadTableData(sid):
    i=0
    tableData=[]
    for key in functions_lookup.keys():
        i+=1
        params=""
        func_inspect=inspect.getfullargspec(functions_lookup[key])
        if len(func_inspect[0])!=0:
            params=",".join(func_inspect[0])
        if func_inspect[1]=="args":
            params+=" *args "
        if func_inspect[2]=="kwargs":
            params+=" *kwargs "
        tableData.append((i, key, params, "http://127.0.0.1:"+str(active_ports[sid])+"/dynamic/"+key))
    return tableData


#? Listen for new user connect
@socketio.on('new user')
def new_user(data):
    global users
    global buffer_ports
    global active_ports
    global tableData
    users += 1
    if len(buffer_ports) == 0:
        active_ports[request.sid] = 5000+users
    else:
        active_ports[request.sid] = buffer_ports.pop()
    tableData = loadTableData(request.sid)
    print('New Client Connected!')

#?Listen for Use Service Button Click
@socketio.on('start service')
def start_service(data):
    global tableData
    windowTitle = "service" + str(active_ports[request.sid])
    #command = "python service.py " + str(active_ports[request.sid]) + " " + data['data']
    command = "python service.py " + str(active_ports[request.sid])
    #p=subprocess.Popen("python service.py " + str(active_ports[request.sid]), shell=True, stdin=subprocess.PIPE)
    os.system('start "'+ windowTitle +'" cmd /k ' + command)
    emit('show table', {'tableData': tableData})


#?Listen for disconnection events
@socketio.on('disconnect')
def test_disconnect():
    global users
    global buffer_ports
    global active_ports
    
    #Kill that service on specific port
    for proc in process_iter():
        for conns in proc.connections(kind='inet'):
            if conns.laddr.port == active_ports[request.sid]:
                proc.send_signal(SIGTERM)  # or SIGKILL

    users -= 1
    buffer_ports.append(active_ports[request.sid])
    del active_ports[request.sid]

    print('A Client disconnected!')


#?Render home template
@app.route('/', methods=['GET','POST'])
def home():
    if (request.method == 'GET'):
        return render_template('home.html'), 200



if __name__ == '__main__':
    socketio.run(app)

