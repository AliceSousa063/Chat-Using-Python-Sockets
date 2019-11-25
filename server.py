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
        msg = clientsocket.recv(2048)
        msg = dict(pickle.loads(msg))
        print(msg)

        for send in clients:
            # print(f'msg = {msg["FROM"]}')
            # print(f'send[1] = {send[1]}')
            #Caso o usuário envie para ele mesmo ou para algum usuário inexistente
            if send[1] == msg["FROM"]:
                print('a')
                msg = {"FROM": 'SERVER', "SUB": 'ERRORR!!!', "MSG": 'You are sending to yourself or recipient does not exist!!!'}
                msg = pickle.dumps(msg)
                clientsocket.send(msg)

            if send[1] in msg["TO"]:
                print('b')
                msg = pickle.dumps(msg)
                send[0].send(msg)


def new_connection():

    #Conectando um novo cliente ao servidor
    clientsocket, address = server.accept()

    #Testando caso o nome de usuário ja esteja sendo usado
    existing_user = True
    client_name = ''
    while existing_user:
        client_name = clientsocket.recv(32).decode('utf-8')  #Recebendo o nome de usuário do cliente
        if len(clients) == 0:
            existing_user = False
        else:
            for name in clients:
                if name[1] == client_name:
                    clientsocket.send(bytes('FAILED', 'utf-8'))
                else:
                    existing_user = False
    clientsocket.send(bytes('ACCEPT', 'utf-8'))

    global num_conections
    num_conections += 1

    #Messagem de boas vindas para o novo cliente
    print(f'Nova conexão!!!')
    msg = {"FROM": 'Server', "MSG": 'Welcome to my server!!!'}
    msg = pickle.dumps(msg) #Transformando o dicionário em string
    clientsocket.send(msg)

    clients.append((clientsocket, client_name)) #Salvando o socket do cliente e o nome de usuário
    print(clients)
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
