import socket
import threading
import joblib
import os

model = joblib.load('my_model.pkl')
def start(line, client):
    print(f'Connected: {client}')
    while True:
        try:
            data = line.recv(1024).decode()
            if not data: break
            
            features = [float(x) for x in data.split(',')]
            
            # -------predict-----
            prediction = model.predict([features])
            
            if prediction[0] == 1:
                status = "ATTACK!"
                # 
                line.sendall(b"BLOCK") 
            else:
                status = "NORMAL"
                
                line.sendall(b"OK")
            
            print(f"Result for {client}: {status}")
            
            # ---save----
            with open('logs.txt', 'a') as f:
                f.write(f"Client {client} | Result: {status} | Data: {data}\n")
        except:
            break
    line.close()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
enter_ip_vps = input('enter the ip of vps >> ')
enter_port_vps = int(input('enter the port of vps >> '))
server.bind((enter_ip_vps, enter_port_vps))
server.listen(7)
print("Security Server started on port 5000...")

while True:
    line, client = server.accept()
    threading.Thread(target=start, args=(line, client), daemon=True).start()
