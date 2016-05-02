import socket
import sys
import threading

all_connections = []
all_addresses = []

# -----------------CREATE SOCKET----------------- #

def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 9977
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print("Socket creation error " + str(msg))

# -----------------BIND SOCKET----------------- #

def socket_bind():
    try:
        global host
        global port
        global s
        print("Binding socket to port " + str(port))
        s.bind((host, port)) # tuple
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error " + str(msg) + "\n" + "Retrying...")
        socket_bind()

# -----------------THREAD FOR LISTENING TO INCOMING DATA----------------- #

class startThreadClass(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        listening_for_msgs(self.conn)


# -----------------ACCEPT CONNECTIONS FROM MULTIPLE CLIENTS----------------- #

def accept_connections():
    try:
        for c in all_connections:
            c.close()
            del all_connections[:]
            del all_addresses[:]
        while 1:
            try:
                conn, address = s.accept()
                conn.setblocking(1) # I dont want any time out
                all_connections.append(conn)
                all_addresses.append(address)

                startThread = startThreadClass(conn)
                startThread.start()

                print("\nConnection has been established: " + address[0]) # Printing out the IP address
            except:
                print("Error accepting connections")
    except KeyboardInterrupt:
        sys.exit()
# -----------------SENDS FILE WHEN CLIENT REQUESTS FOR HTML FILE ----------------- #


def send_file(conn, msg):
    file_content = ''
    if msg == 'server':
        with open('clientHTML.html') as f:
            for line in f:
                file_content += line
            conn.send(str.encode(file_content, 'utf-8'))
            f.close()
    elif msg == "/Users/nyavuz/Desktop/program/clicked_link.html":
        with open('clicked_link.html') as f:
            for line in f:
                file_content += line
            conn.send(str.encode(file_content, 'utf-8'))
            f.close()
    elif msg == "/Users/nyavuz/Desktop/program/clicked2_link.html":
        with open('clicked2_link.html') as f:
            for line in f:
                file_content += line
            conn.send(str.encode(file_content, 'utf-8'))
            f.close()
# -----------------LISTEN FOR INCOMING DATA FUNCTION----------------- #


def listening_for_msgs(conn):
    while True:
        try:
            rcv_msg = conn.recv(1024)
            rcv_msg_str = str(rcv_msg[:].decode("utf-8"))
            if rcv_msg_str == 'server':
                send_file(conn, "server")
            elif rcv_msg_str == '/Users/nyavuz/Desktop/program/clicked_link.html':
                send_file(conn, rcv_msg_str)
            elif rcv_msg_str == '/Users/nyavuz/Desktop/program/clicked2_link.html':
                send_file(conn, rcv_msg_str)
            else:
                pass

        except UnicodeDecodeError:
            pass

# -----------------MAIN FUNCTION----------------- #

def main():
    socket_create()
    socket_bind()
    accept_connections()

main()
