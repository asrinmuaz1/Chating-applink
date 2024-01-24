import tkinter as tk
import socket
import json

MAX_GROUP_SIZE = 15

def login():
    username = username_entry.get()
    password = password_entry.get()

    login_info = {'username': username, 'password': password}
    login_info_json = json.dumps(login_info)

    client_socket.send(login_info_json.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    print(response)

    if "successful" in response:
        # Başarılı giriş durumunda arkadaş listesini güncelle
        friends_listbox.delete(0, tk.END)
        friends_listbox.insert(tk.END, *get_friends_list(response))

def get_friends_list(response):
    # Sunucudan gelen yanıtı parse edip arkadaş listesini al
    start_index = response.find("[")  # Arkadaş listesi JSON'ının başlangıcı
    end_index = response.find("]") + 1  # Arkadaş listesi JSON'ının sonu
    friends_json = response[start_index:end_index]
    friends_list = json.loads(friends_json)
    return friends_list

def add_friend():
    friend_code = friend_code_entry.get()
    add_friend_info = {'action': 'add_friend', 'friend_code': friend_code}
    add_friend_info_json = json.dumps(add_friend_info)

    client_socket.send(add_friend_info_json.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    print(response)

    if "successful" in response:
        # Başarılı arkadaş ekleme durumunda arkadaş listesini güncelle
        friends_listbox.delete(0, tk.END)
        friends_listbox.insert(tk.END, *get_friends_list(response))

def create_group():
    group_name = group_name_entry.get()
    selected_friends = friends_listbox.curselection()

    if not group_name:
        print("Please enter a group name.")
        return

    if not selected_friends:
        print("Please select friends to add to the group.")
        return

    if len(selected_friends) > MAX_GROUP_SIZE:
        print(f"A group can have at most {MAX_GROUP_SIZE} members.")
        return

    group_members = [friends_listbox.get(index) for index in selected_friends]
    create_group_info = {'action': 'create_group', 'group_name': group_name, 'group_members': group_members}
    create_group_info_json = json.dumps(create_group_info)

    client_socket.send(create_group_info_json.encode('utf-8'))
    print(f"Group '{group_name}' created with members: {', '.join(group_members)}")

# İstemci GUI
client_window = tk.Tk()
client_window.title("User Login")

# Kullanıcı adı ve şifre için Entry'ler
username_label = tk.Label(client_window, text="Username:")
username_label.pack(pady=10)

username_entry = tk.Entry(client_window, width=30)
username_entry.pack(pady=10)

password_label = tk.Label(client_window, text="Password:")
password_label.pack(pady=10)

password_entry = tk.Entry(client_window, width=30, show="*")
password_entry.pack(pady=10)

# Giriş yapma butonu
login_button = tk.Button(client_window, text="Login", command=login)
login_button.pack(pady=20)

# Arkadaş ekleme için Entry ve Button
friend_code_label = tk.Label(client_window, text="Friend's Code:")
friend_code_label.pack(pady=10)

friend_code_entry = tk.Entry(client_window, width=30)
friend_code_entry.pack(pady=10)

add_friend_button = tk.Button(client_window, text="Add Friend", command=add_friend)
add_friend_button.pack(pady=20)

# Arkadaş listesi için ListBox
friends_listbox = tk.Listbox(client_window, width=40, height=10, selectmode=tk.MULTIPLE)
friends_listbox.pack(pady=10)

# Grup oluşturma için Entry ve Button
group_name_label = tk.Label(client_window, text="Group Name:")
group_name_label.pack(pady=10)

group_name_entry = tk.Entry(client_window, width=30)
group_name_entry.pack(pady=10)

create_group_button = tk.Button(client_window, text="Create Group", command=create_group)
create_group_button.pack(pady=20)

# Sunucu ile bağlantı
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 5555))

# İstemci GUI'nin başlatılması
client_window.mainloop()
