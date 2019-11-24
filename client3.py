import socket
import pickle
from threading import Thread

IP = '127.0.0.1'
PORT = 1234
my_username = input('Username: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

#Recebendo menssagem de boas vindas do servidor
welcome = client.recv(1024)
welcome = pickle.loads(welcome)
print(f'{welcome["FROM"]} says: {welcome["MSG"]}')

#Enviando o nome de usuário para o servidor
client.send(bytes(f'{my_username}', 'utf-8'))

wait_to_send = 0
wait_to_receive = 0


#Função responsável por enviar a menssagem
def send():
    to = ''
    msg = ''

    while to == '':
        to = input('To > ')

    sub = input('Subject > ')

    while msg == '':
        msg = input(f'{my_username} > ')

    msg_to_send = {"TO": f'{to}', "FROM": f'{my_username}', "SUB": f'{sub}', "MSG": f'{msg}'}
    msg_to_send = pickle.dumps(msg_to_send)
    client.send(msg_to_send)
    global wait_to_send
    wait_to_send = 0


#Função responsável por receber a menssagem
def receive():
    msg = client.recv(1024)
    msg = pickle.loads(msg)

    print(f'\n-----{msg["FROM"]}-----\nSubject > {msg["SUB"]} \nMessage > {msg["MSG"]}')
    print('-' * (len(msg["FROM"]) + 10))

    global wait_to_receive
    wait_to_receive = 0


while True:
    if wait_to_send == 0:
        '''
        A estrategia adotada nesse caso foi usar uma variavel 
        de controle para que haja apenas uma ação de envio.  
        '''
        wait_to_send += 1
        #Criando uma thread para enviar uma menssagem
        Thread(target=send).start()

    if wait_to_receive == 0:
        '''
        A estrategia adotada nesse caso foi usar uma variavel 
        de controle para que haja apenas uma ação de recebimento.  
        '''
        wait_to_receive += 1
        #Criando uma thread para receber uma menssagem
        Thread(target=receive).start()
