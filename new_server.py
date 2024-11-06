import socket#导入整个模块，使用时需通过模块名访问模块中的对象
import os

# 定义函数start_server，用于启动一个UDP服务器。
# 函数接受两个参数，host表示服务器监听的IP地址，默认值为'214.0.0.1'（本地回环地址），port表示服务器监听的端口号，默认值为12000
#def创建一个类
def start_server(host='127.0.0.1', port=12000):  
    # 创建一个基于IPv4（socket.AF_INET）和UDP协议（socket.SOCK_DGRAM）的套接字对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    #try...except...else用于异常处理，try用于检测，except用于捕获try后的异常信息并处理，else为无异常现象则执行其后的语句
    try:
        # 将创建好的套接字绑定到指定的主机地址和端口号上
        # 这样服务器就可以在这个地址和端口上监听来自客户端的数据
        server_socket.bind((host, port))  
        print(f'Server is listening on {host}:{port}')  

        # 进入一个无限循环，持续监听并处理客户端的请求
        while True:  
            # 从客户端接收数据，最多接收1024字节。recvfrom函数返回两个值，
            # 一个是接收到的数据（bytes类型），另一个是发送数据的客户端地址（包含IP和端口的元组）
            data, client_address = server_socket.recvfrom(1024)  
            # 将接收到的字节数据解码为字符串，并检查是否等于'SEND_FILE'。
            # 如果等于，表示客户端准备发送文件
            if data.decode() == 'SEND_FILE':  
                # 接收文件名，最多接收1024字节。同样返回数据和客户端地址，这里我们只关心文件名数据
                filename_bytes, _ = server_socket.recvfrom(1024)  
                # 将接收到的文件名字节数据解码为字符串
                filename = filename_bytes.decode()  
                print(f'Receiving file named: {filename}')  
                try:
                    # 以二进制写入模式打开文件。如果文件不存在，将创建新文件；如果文件已存在，将覆盖原有内容
                    with open(filename, 'wb') as f:  
                        while True:  
                            # 从客户端接收文件内容数据块，最多接收1024字节，以及客户端地址
                            bytes_packet, client_address = server_socket.recvfrom(1024)  
                            # 如果接收到的字节数据为空，表示文件传输结束
                            if not bytes_packet:
                                break  
                            # 将接收到的字节数据块写入文件
                            f.write(bytes_packet)  
                    print(f'The file named {filename} received successfully.')  
                except Exception as e:
                    print(f"Error while writing file: {e}")
    except Exception as e:
        print(f"Server startup error or bind error: {e}")
    finally:
        # 关闭套接字，释放系统资源。无论是否出现异常，都要执行这一步
        server_socket.close()


if __name__ == "__main__":  
    start_server()