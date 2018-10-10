

# 这是客户端程序接受数据
import socket,threading,time
import struct
import pygame
import cv2
import numpy as np
ADDRESS = ('192.168.43.153', 12801)
IMAGE_SIZE = (640, 480)

# 显示操作
pygame.init()
screen = pygame.display.set_mode((800, 600))
screen_rect = screen.get_rect()
clock = pygame.time.Clock()

s = socket.socket()
s.connect(ADDRESS)
print('connected')

while True:
    try:
        len_str = s.recv(4)
        size = struct.unpack('!i', len_str)[0]
        print('size:', size)

        img_str = b''

        while size > 0:
            if size >= 4096:
                data = s.recv(4096)
                # print('oo')
            else:
                data = s.recv(size)

            if not data:
                break

            size -= len(data)
            img_str += data
        print('len:', len(img_str))
                # 将字节数据转换为图像数据
        image = pygame.image.fromstring(img_str, IMAGE_SIZE, "RGB")
        # data = pygame.surfarray.array2d(image)
        # print(data.shape)
        # image = np.array(image)
        image_rect = image.get_rect(center=screen_rect.center)
        screen.blit(image, image_rect)
        pygame.display.flip()
        # print(data)
        # cv2.imshow('1', data)
    except Exception as e:
        print(e)




        

