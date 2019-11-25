import socket
import pickle
from time import sleep
from threading import Thread

IP = '127.0.0.1'
PORT = 1234
my_username = ''

while my_username == '':
    my_username = input('User name: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

#Enviando o nome de usuário para o servidor
client.send(bytes(f'{my_username}', 'utf-8'))

#Verificando se o nome de usuário é valido
checking = True
while checking:
    msg = client.recv(1024).decode('utf-8')
    print(msg)
    if msg == 'ACCEPT':
        checking = False
    else:
        my_username = input('User name: ')
        client.send(bytes(f'{my_username}', 'utf-8'))


#Recebendo menssagem de boas vindas do servidor
welcome = client.recv(1024)
welcome = pickle.loads(welcome)
print(f'{welcome["FROM"]} says: {welcome["MSG"]}')

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
        msg = input('Message > ')

    msg_to_send = {"TO": f'{to}', "FROM": f'{my_username}', "SUB": f'{sub}', "MSG": f'{msg}'}
    msg_to_send = pickle.dumps(msg_to_send)
    client.send(msg_to_send)
    sleep(1)
    global wait_to_send
    wait_to_send = 0
    print('\n')



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
