import socket
import pickle
from threading import Thread

'''
O modulo pickle é responsável por transformar objetos em strings,
atraves dessa transformação podemos enviar qualquer tipo de estrutura em python,
desde listas, dicionários, até classes.
'''

'''
O modulo threading usando o método Thread é responsavel pelos processos
de envio e recebimento ocorrerem em paralelo.
'''

IP = '127.0.0.1'
PORT = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((IP, PORT))
server.listen(5)

num_conections = 0
num_threads = 0

clients = []

def msg_manager(clientsocket):
    while True:
        msg = clientsocket.recv(1024)
        msg = pickle.loads(msg)
        print(msg)

        for send in clients:
            if send[1] == msg["TO"]:
                msg = pickle.dumps(msg)
                send[0].send(msg)


def new_connection():

    #Conectando um novo cliente ao servidor
    clientsocket, address = server.accept()

    global num_conections
    num_conections += 1

    #Messagem de boas vindas para o novo cliente
    print(f'Nova conexão!!!')
    msg = {"FROM": 'Server', "MSG": 'Welcome to my server!!!'}
    msg = pickle.dumps(msg) #Transformando o dicionário em string
    clientsocket.send(msg)

    client_name = clientsocket.recv(32).decode('utf-8') #Recebendo o nome de usuário do cliente
    clients.append((clientsocket, client_name)) #Salvando o socket do cliente e o nome de usuário
    msg_manager(clientsocket)


while True:
    if num_conections == num_threads:
        '''
        A estratégia adotada nesse caso foi, ter sempre uma thread
        a mais do que conexões em que essa thread à mais estara 
        esperando uma nova conexão.
        '''
        Thread(target=new_connection).start()
        num_threads += 1
