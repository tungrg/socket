from socket import *
from datetime import datetime

default_host = 'localhost'
port = 9000
Format = 'utf-8'
true_username = 'admin'
true_password = 'admin'
ADDRESS = (default_host,port)
default_page = "index.html"
info_page = "info.html"
not_found = "404.html"

def createServer():
    #khởi tạo server với IPv4, giao thức TCP
    serverSocket = socket(AF_INET, SOCK_STREAM)
    #bind tại địa chỉ và port
    serverSocket.bind(ADDRESS)
    return serverSocket
def Start(server):

    try:
        #sever nghe client request
        server.listen()
        while(1):
            #chấp nhận kết nối, khởi tạo client socket
            (client_socket,adddress) = server.accept()
            #nhận request
            rd = client_socket.recv(5000).decode()

            #xuất request
            print(rd + "\n\n")

            #phân tích dữ liệu theo từng dòng
            piece = rd.split("\n")

            #kiểm tra method của request
            METHOD = piece[0].split(' ')[0]

            #nếu client yêu cầu get dữ liệu:
            if(METHOD == "GET"):
                #lấy file mà client cần GET
                request_file = piece[0].split(' ')[1]
                request_file = request_file.lstrip('/')

                #nếu là địa chỉ mặc định
                if(request_file == ""):
                    request_file = default_page
                
                #xử lý file
                f = open(request_file, "rb")
                filedata = f.read()
                filelength = len(filedata)
                f.close()
                #tạo buffer để respone dữ liệu cho client
                #tạo header 
                buffer = "HTTP/1.1 200 OK\r\n"
                buffer += "Server: PYTHON server \r\n"
                buffer += "Date: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\r\n"
                buffer += "Content-length: " + str(filelength) + "\r\n"
                buffer += "Content-Type: "
                #thêm vào đuôi các định dạng file nếu có yêu cầu
                if request_file.endswith(".ico"):
                    buffer += "image/ico"
                elif request_file.endswith(".html"):
                    buffer += "text/html"
                elif request_file.endswith(".jpg"):
                    buffer += "image/jpg"
                elif request_file.endswith(".jpeg"):
                    buffer += "image/jpeg"
                elif request_file.endswith(".css"):
                    buffer += "text/css"
                elif request_file.endswith(".woff"):
                    buffer += "font/woff"
                elif request_file.endswith(".woff2"):
                    buffer += "font/woff2" 
                buffer += "\r\n\r\n"

                #encode lại buffer để chuẩn bị thêm dữ liệu từ file vào
                buffer = buffer.encode('utf-8')

                #thêm dữ liệu của file vào buffer
                buffer += filedata
            #nếu client yêu cầu get dữ liệu
            elif (METHOD =="POST"):
                #Phần data của buffer
                check = piece[-1]

                #xử lý data
                username = check[check.index("username") + 9: check.index("&password")]
                password = check[check.index("&password") + 10: len(check)]
                #so sánh với tài username và password mặc định
                if(username == true_username and password == true_password):
                    #chuyển hướng client tới trang info
                    buffer = 'HTTP/1.1 303 See Other\nLocation:' + info_page + '\n'
                else:
                    #chuyển hướng client tới trang 404
                    buffer = 'HTTP/1.1 303 See Other\nLocation:' + not_found + '\n'
                #endcode lại buffer để gửi đi
                buffer = buffer.encode('utf-8')
            
            client_socket.sendall(buffer)
            #đóng client socket
            client_socket.shutdown(SHUT_WR)
    except KeyboardInterrupt :
        print("\nShutting down...\n")
    except Exception as exc :
        print("Error:\n")
        print(exc)
    
    
    #đóng server socket
    server.close()

print('access localhost:9000')
servertest = createServer()
Start(servertest)
