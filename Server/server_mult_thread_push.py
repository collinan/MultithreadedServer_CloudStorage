#Author: Andrew Collins:
#Description: Server that allows processing of clients in parallel using threads.
#Data collected on server is pushed to the cloud using Google Sheets API.

#for passing argument in
import sys
from datetime import datetime
import gspread
import time

#import socket library ,able to use socket object
import socket

from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

# import thread module
from _thread import *
import threading


print_lock = threading.Lock()
#-----------------------------------------------------------------------------

#----------Start function: main()----------
def Main():
    host = '10.249.222.248'

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 8090

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to post", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        conn, addr = s.accept()
        ip = addr[0]
        port = addr[1]
        # lock acquired by client
        print_lock.acquire()
        #print('Connected to:', addr[0], ':', addr[1])
        # Start a new thread and return its identifier
        start_new_thread(threaded, (conn,ip,port))
    s.close()

#----------End function: main()----------


#----------Start function: threaded()----------
def threaded(conn,ip,port):

    from_client = ''
    data = b''
    EOL1 = b'\r\n'
    connect_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #print("Got a connection from %s" % str(addr))
    while EOL1 not in data:
        data += conn.recv(1024)

    print_lock.release()
        #if not data: break
        #print("here")

    from_client += data.decode()
    client_id=str(from_client.rstrip("\r\n").split(',')[0])
    print("Connected to client ID:%s  at port %s at time %s." % (client_id, port,connect_time))

    if client_id == '111001':
        print("Clinet %s sleeping 10 seconds."% (client_id))
        time.sleep(10)
    elif client_id == '111002':
        print("Clinet %s sleeping 20 seconds."% (client_id))
        time.sleep(20)
    elif client_id == '111003':
        print("Clinet %s sleeping 30 seconds."% (client_id))
        time.sleep(30)
    elif client_id == '111004':
        print("Clinet %s sleeping 40 seconds."% (client_id))
        time.sleep(40)
    else:
        print("Clinet %s sleeping 50 seconds."% (client_id))
        time.sleep(50)




    server_msg_send= 'Message recieved: '+connect_time+"\r\n"
    #print( from_client)
    conn.send(server_msg_send.encode('ascii'))
    conn.close()
    print("Client disconnected %s at time %s.\n"% (client_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    google_push(from_client,connect_time)
#----------End function: threaded()----------
#----------Start function: google_push()----------
#function pushes clients message to google sheets
def google_push(msg_push,connect_time):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("DataLoggingCreds.json",scope)#replace with your credentials file
    client = gspread.authorize(credentials)

    msg_push = msg_push.rstrip("\r\n")+","+ "Server Connect Time:,"+connect_time+",Pushed to sheet time:,"+datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #print(msg_push)
    #print(msg_push.split(','))
    sheet =client.open("DataFile").sheet1
    insertRow = [ msg_push ]

    sheet.append_row(msg_push.rstrip().split(','))
    return;
#----------End function: google_push----------

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    Main()
