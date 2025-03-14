import socket
import time

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))

    try:
        while True:
            message = "Hello from client"
            client_socket.send(message.encode('utf-8'))
            print(f"发送消息: {message}")
            time.sleep(5)  # 每5秒发送一次心跳消息
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
