

from sshtunnel import SSHTunnelForwarder

server = SSHTunnelForwarder(
    ('172.16.1.22', 22),#Step 2连接远端服务器SSH端口
    ssh_username="root",
    ssh_password="Cisc0123",
    local_bind_address=('202.100.1.224',8080),#Step 1连接本地地址'202.100.1.224',8080
    remote_bind_address=('127.0.0.1', 80)#Step 3跳转到远端服务器'127.0.0.1', 80
)

server.start()

print(server.local_bind_port)#如果不配置local_bind_address,将会随机绑定本地端口，并且打印

#server.stop()
