
import socket,threading,time
import struct
import PARAM


# 这份代码是sever啊
ADDRESS = (PARAM.Server_addr, 12801)
def senddata():
    s = socket.socket()

    # solution for: "socket.error: [Errno 98] Address already in use"
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(ADDRESS)
    # 开始监听
    s.listen()
    i = 0
    try:
         sc, info = s.accept()
         print('client connected:', info)
         while True:
             if PARAM.BMP_FLAG:
                 i += 1
                 print(i)
                 # print()
                 len_img = len(PARAM.IMAGE_STORE)
                 print('len:', len_img)
                 # send string size
                
                 len_str = struct.pack('!i', len_img)
                 sc.send(len_str)

                 # send string image
                
                 sc.send(PARAM.IMAGE_STORE)

                 # 一次传输完成后将标志位flag置0
                 PARAM.BMP_FLAG = 0
    except Exception as e:
        print(e)
    finally:
        s.close()



