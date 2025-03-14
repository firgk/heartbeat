#include <ESP8266WiFi.h>

// WiFi 信息
const char* ssid = "lghk669";          // WiFi 名称
const char* password = "aaaaaaaa";  // WiFi 密码

// 服务器 IP 和端口
const char* server_ip = "192.168.117.1"; // 服务器 IP 地址
const int server_port = 12345;           // 服务器端口

WiFiClient client;

void setup() {
  // 启动串口通信
  Serial.begin(115200);
  
  // 连接 WiFi
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi!");

  // 连接服务器
  connectToServer();
}

void loop() {
  // 每隔 5 秒发送消息
  if (client.connected()) {
    String message = "nas network right!";
    client.println(message);
    Serial.println("Message sent: " + message);
    delay(5000); // 5秒发送一次消息
  } else {
    // 如果连接断开，重新连接
    connectToServer();
  }
}

void connectToServer() {
  Serial.println("Connecting to server...");
  // 连接服务器
  while (!client.connect(server_ip, server_port)) {
    Serial.println("Connection failed, retrying...");
    delay(1000);
  }
  Serial.println("Connected to server!");
}
