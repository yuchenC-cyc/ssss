import socket  
import sys  #引入sys模块
import os  #os库中的os.path字库用于操作和处理文件路径

# 定义函数send，用于向指定服务器发送文件
# s_ip：服务器的IP地址
# s_port：服务器的端口号
# file_path：要发送的文件在本地的路径
def send(s_ip, s_port, file_path):  
    # 创建一个基于IPv4（socket.AF_INET）和UDP协议（socket.SOCK_DGRAM）的套接字对象
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    # 检查指定的文件路径是否是一个文件，如果不是，则打印错误信息并退出程序
    if not os.path.isfile(file_path):  
        print(f"The file named {file_path} not a file or not found")  
        sys.exit(1)
    # 获取要发送文件的文件名（去除路径部分）
    filename = os.path.basename(file_path)  
    # 向服务器发送指令'SEND_FILE'，告知服务器准备发送文件。
    # b'SEND_FILE'将字符串转换为字节类型，因为套接字通信发送的是字节数据
    c_socket.sendto(b'SEND_FILE', (s_ip, s_port))  
    # 向服务器发送文件名，将文件名编码为字节类型后发送
    c_socket.sendto(filename.encode(), (s_ip, s_port))  

    # 以二进制读取模式打开要发送的文件
    #as f部分将打开的文件对象（由open函数返回）赋值给变量f。这样，在with语句块内部，就可以使用f这个变量来代表打开的文件，从而方便地对文件进行操作。
    with open(file_path, 'rb') as f:  
        # 从文件中读取最多1024字节的数据
        bytes_read = f.read(1024)  
        # 只要读取到的数据长度大于0，就继续循环发送数据
        while bytes_read:  
            c_socket.sendto(bytes_read, (server_ip, server_port))  
            # 继续读取下一个1024字节的数据
            bytes_read = f.read(1024)  

    print(f'File {filename} sent successfully.')  
    # 关闭套接字，释放资源
    c_socket.close()  

if __name__ == "__main__":  
    # 检查命令行参数的数量是否为4
    #不为4则退出程序
    if len(sys.argv)!= 4:  
        print("Error usage way in parameter")    
	#退出程序
        sys.exit(1)
    # 获取命令行参数中的服务器IP地址
    s_ip = sys.argv[1]  
    # 获取命令行参数中的服务器端口号，并转换为整数类型
    s_port = int(sys.argv[2])  
    # 获取命令行参数中的要发送文件的本地路径
    file_path = sys.argv[3]  
    #输入所需的三个参数
    send(s_ip, s_port, file_path)  