import pygame

pygame.init()
# kích thước của bàn cờ
Height = 700
Width = 1000
# font và cỡ chứ
font = pygame.font.SysFont("Arial", 20)
bigfont = pygame.font.SysFont("Arial", 50)
#màn hình
screen = pygame.display.set_mode((Width, Height))
fps = 60

#piece
whitePiece = ['xeT', 'maT', 'tuongT', 'vuaT', 'hauT', 'tuongT', 'maT', 'xeT',
              'totT', 'totT','totT', 'totT','totT', 'totT','totT', 'totT']
blackPiece = ['xeD', 'maD', 'tuongD', 'vuaD', 'hauD', 'tuongD', 'maD', 'xeD',
              'totD', 'totD','totD', 'totD','totD', 'totD','totD', 'totD']
xeTImg = pygame.image.load("images/white rook.png")
xeTImg = pygame.transform.scale(xeTImg, (60, 60))

maTImg = pygame.image.load("images/white knight.png")
maTImg = pygame.transform.scale(maTImg, (60, 60))

tuongTImg = pygame.image.load("images/white knight.png")
tuongTImg = pygame.transform.scale(tuongTImg, (80, 80))

vuaTImg = pygame.image.load("images/white knight.png")
vuaTImg = pygame.transform.scale(vuaTImg, (80, 80))

hauTImg = pygame.image.load("images/white knight.png")
hauTImg = pygame.transform.scale(vuaTImg, (80, 80))

totTImg = pygame.image.load("images/white knight.png")
totTImg = pygame.transform.scale(totTImg, (60, 60))



pygame.display.set_caption("Chess")
'''
    bàn cờ có 8x8 ô, mỗi ô có kích thước Width/8 x Height/8
    bên phải bàn cờ sẽ có 1 hình chữ nhật màu xám để hiển thị các nước đi, các quân cờ đã mất của 2 bên
    hiển thị cả thời gian
    status
'''
def draw_board():
    for i in range(8):
        for j in range(8):
            if (i+j)%2 == 0:
                pygame.draw.rect(screen, "gray", (i*Height/8, j*Height/8, Height/8, Height/8))
            else:
                pygame.draw.rect(screen, "black", (i*Height/8, j*Height/8, Height/8, Height/8))
    
    pygame.draw.rect(screen, 'gray',(Height, 0, Width - Height, Height))
    pygame.draw.line(screen, 'gold', (Height, 0),(Height, Height), width = 2)
    
    status_board = ["white move", "black move"]      
    screen.blit(bigfont.render(status_board[0], True, 'black'), (Height + 20, 20))  

# vẽ quân cờ lên bàn cờ
def drawPiece():
    screen.blit(xeTImg, (10, 10))

while(True):
    screen.fill("white")
    draw_board()
    drawPiece()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    
    pygame.display.flip()
    pygame.time.Clock().tick(fps)
    
