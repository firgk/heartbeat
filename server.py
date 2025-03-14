import socket
import threading
import time
from flask import Flask, render_template

app = Flask(__name__)

# 存储客户端连接状态
clients = {}

# 客户端消息监听线程
def listen_for_clients():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))  # 监听所有网络接口
    server_socket.listen(5)
    print("服务器启动，等待客户端连接...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"客户端 {client_address} 连接成功")
        
        # 每个客户端用线程进行管理
        threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()

# 处理客户端请求
def handle_client(client_socket, client_address):
    global clients
    client_socket.settimeout(10)  # 设置超时时间（10秒）

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                clients[client_address] = '在线'  # 客户端发送消息时为在线状态
                print(f"收到来自 {client_address} 的消息: {message}")
            else:
                clients[client_address] = '离线'  # 如果没有消息，认为客户端已离线
        except socket.timeout:
            clients[client_address] = '离线'  # 客户端超时没有数据，认为离线
            break
        except Exception as e:
            clients[client_address] = '离线'
            print(f"错误: {e}")
            break

    client_socket.close()
    print(f"客户端 {client_address} 断开连接")
    # 客户端断开时从字典中删除
    del clients[client_address]

# Flask路由：展示客户端状态
@app.route('/')
def index():
    # 只传递在线的客户端
    online_clients = {client: status for client, status in clients.items() if status == '在线'}
    return render_template('index.html', clients=online_clients)

# 启动Flask应用
def run_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    # 启动客户端监听线程
    threading.Thread(target=listen_for_clients, daemon=True).start()

    # 启动Flask网页展示
    run_flask()
