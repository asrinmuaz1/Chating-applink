import socket
import threading
import json
import secrets

# Kullanıcı bilgilerini, arkadaş listelerini ve grup bilgilerini saklamak için sözlükler
user_credentials = {}
user_friends = {}
user_groups = {}

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        data = data.decode('utf-8')
        data_dict = json.loads(data)

        if 'action' in data_dict:
            action = data_dict['action']

            if action == 'add_friend':
                friend_code = data_dict['friend_code']
                response = add_friend(client_socket, friend_code)
                client_socket.send(response.encode('utf-8'))

            elif action == 'create_group':
                group_name = data_dict['group_name']
                group_members = data_dict['group_members']
                response = create_group(client_socket, group_name, group_members)
                client_socket.send(response.encode('utf-8'))
        else:
            response = authenticate_user(data_dict)
            client_socket.send(response.encode('utf-8'))

def authenticate_user(login_info):
    username = login_info['username']
    password = login_info['password']

    if username in user_credentials and user_credentials[username] == password:
        # Kullanıcı doğrulandı, yeni kod üret ve kullanıcıya gönder
        new_code = secrets.token_hex(16)
        user_credentials[username] = new_code
        friends_list = user_friends.get(username, [])
        response_data = {'status': 'successful', 'new_code': new_code, 'friends_list': friends_list}
    else:
        response_data = {'status': 'failed'}

    return json.dumps(response_data)

def add_friend(client_socket, friend_code):
    for username, code in user_credentials.items():
        if code == friend_code:
            # Arkadaş eklendi
            friends_list = user_friends.get(username, [])
            friends_list.append(client_socket.getpeername()[0])  # İstemcinin IP adresini ekleyebilirsiniz
            user_friends[username] = friends_list
           
