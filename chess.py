import pygame

pygame.init()
# kích thước của bàn cờ
Height = 700
Width = 1000
# font và cỡ chứ
font = pygame.font.SysFont("Arial", 20)
medfont = pygame.font.SysFont("Arial", 30)
bigfont = pygame.font.SysFont("Arial", 50)
#màn hình
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Chess")
#fps
timer = pygame.time.Clock()
fps = 60

#piece of chess
quanTrang = ['xe', 'ma', 'tuong', 'vua', 'hau', 'tuong', 'ma', 'xe',
              'tot', 'tot','tot', 'tot','tot', 'tot','tot', 'tot']
quanDen = ['xe', 'ma', 'tuong', 'vua', 'hau', 'tuong', 'ma', 'xe',
              'tot', 'tot','tot', 'tot','tot', 'tot','tot', 'tot']
viTriTrang = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0),
                 (0,1), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1)]
viTriDen = [(0,7), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7),
                 (0,6), (1,6), (2,6), (3,6), (4,6), (5,6), (6,6), (7,6)]

batTrang = []
batDen = []

# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
doiLuot = 0
luaChon = 100
buocDi = []

# load anh quan co
xeTImg = pygame.image.load("images/white rook.png")
xeTImg = pygame.transform.scale(xeTImg, (60, 60))

maTImg = pygame.image.load("images/white knight.png")
maTImg = pygame.transform.scale(maTImg, (60, 60))

tuongTImg = pygame.image.load("images/white bishop.png")
tuongTImg = pygame.transform.scale(tuongTImg, (80, 80))

vuaTImg = pygame.image.load("images/white king.png")
vuaTImg = pygame.transform.scale(vuaTImg, (80, 80))

hauTImg = pygame.image.load("images/white queen.png")
hauTImg = pygame.transform.scale(hauTImg, (80, 80))

totTImg = pygame.image.load("images/white pawn.png")
totTImg = pygame.transform.scale(totTImg, (60, 60))

xeDImg = pygame.image.load("images/black rook.png")
xeDImg = pygame.transform.scale(xeDImg, (60, 60))

maDImg = pygame.image.load("images/black knight.png")
maDImg = pygame.transform.scale(maDImg, (60, 60))

tuongDImg = pygame.image.load("images/Black bishop.png")
tuongDImg = pygame.transform.scale(tuongDImg, (80, 80))

vuaDImg = pygame.image.load("images/black king.png")
vuaDImg = pygame.transform.scale(vuaDImg, (80, 80))

hauDImg = pygame.image.load("images/black queen.png")
hauDImg = pygame.transform.scale(hauDImg, (80, 80))

totDImg = pygame.image.load("images/black pawn.png")
totDImg = pygame.transform.scale(totDImg, (60, 60))

#tập hợp các quân cờ lại
anhQuanTrang = [xeTImg, maTImg, tuongTImg, vuaTImg, hauTImg, totTImg]
anhQuanDen = [xeDImg, maDImg, tuongDImg, vuaDImg, hauDImg, totDImg]

dsQuan = ["xe", "ma", "tuong", "vua", "hau", "tot"]

# các biến kiểm tra xem game đã kết thúc chưa
counter = 0
winner = ''
game_over = False

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
    
    pygame.draw.rect(screen, 'light gray',(Height, 0, Width - Height, Height))
    pygame.draw.line(screen, 'gold', (Height, 0),(Height, Height), width = 2)
    # hiển thị lượt đi của các bên
    status_text = ["white: select a piece", "white: move a piece", "black: select a piece", "black: move a piece"]      
    screen.blit(medfont.render(status_text[0], True, 'black'), (Height + 20, 20))  

# vẽ quân cờ lên bàn cờ
def drawPiece():
    for i in range(len(quanTrang)):
        idx = dsQuan.index(quanTrang[i])
        if dsQuan[idx] == 'tot':
            screen.blit(anhQuanTrang[idx], (viTriTrang[i][0]*Height/8 + 10, viTriTrang[i][1]*Height/8 + 20))
        else:
            if dsQuan[idx] == 'xe' or dsQuan[idx] == 'ma':
                screen.blit(anhQuanTrang[idx], (viTriTrang[i][0]*Height/8 + 10, viTriTrang[i][1]*Height/8 + 20))
            else:
                screen.blit(anhQuanTrang[idx], (viTriTrang[i][0]*Height/8, viTriTrang[i][1]*Height/8))

    for i in range(len(quanDen)):
        idx = dsQuan.index(quanDen[i])
        if dsQuan[idx] == 'tot':
            screen.blit(anhQuanDen[idx], (viTriDen[i][0]*Height/8 + 10 , viTriDen[i][1]*Height/8 + 20))
        else:
            if dsQuan[idx] == 'xe' or dsQuan[idx] == 'ma':
                screen.blit(anhQuanDen[idx], (viTriDen[i][0]*Height/8 + 10, viTriDen[i][1]*Height/8 + 20))
            else:
                screen.blit(anhQuanDen[idx], (viTriDen[i][0]*Height/8, viTriDen[i][1]*Height/8))
         
# vẽ các nước đi và các quân cờ đã mất
def draw_moves(vitri, dsQuan, luot):
    moves = []
    allMoves = []
    for i in range(len(dsQuan)):
        viTri = vitri[i]
        quan = dsQuan[i]
        if quan == 'xe':
            moves = getMoveRook(viTri[0], viTri[1], luot)
        elif quan == 'ma':
            moves = getMoveKnight(viTri[0], viTri[1], luot)
        elif quan == 'tuong':
            moves = getMoveBishop(viTri[0], viTri[1], luot)
        elif quan == 'vua':
            moves = getMoveKing(viTri[0], viTri[1], luot)
        elif quan == 'hau':
            moves = getMoveQueen(viTri[0], viTri[1], luot)
        elif quan == 'tot':
            moves = getMovePawn(viTri[0], viTri[1], luot)
        allMoves.append(moves)
        return allMoves

def getMovePawn(vitri, luot):
    moveList = []
    if luot == 'T':
        if (vitri[0], vitri[1]+ 1) not in viTriTrang and (vitri[0], vitri[1]+ 1) not in viTriDen and vitri[1] < 7:
            moveList.append((vitri[0], vitri[1] + 1))
        elif (vitri[0], vitri[1]+ 2) not in viTriDen and (vitri[0], vitri[1] + 2) not in viTriTrang and vitri[1] < 7:
            
            moveList.append((vitri[0], vitri[1] + 2))
        elif (vitri[0] + 1, vitri[1] + 1) in viTriDen:
            moveList.append((vitri[0] + 1, vitri[1] + 1))
        elif (vitri[0] - 1, vitri[1] + 1) in viTriDen:
            moveList.append((vitri[0] - 1, vitri[1] + 1))
    else:
        if (vitri[0], vitri[1] - 1) not in viTriTrang and (vitri[0], vitri[1] - 1) not in viTriDen and vitri[1] < 7:
            moveList.append((vitri[0], vitri[1] - 1))
        elif (vitri[0], vitri[1] - 2) not in viTriDen and (vitri[0], vitri[1] - 2) not in viTriTrang and vitri[1] < 7:
            moveList.append((vitri[0], vitri[1] - 2))
        elif (vitri[0] + 1, vitri[1] - 1) in viTriTrang:
            moveList.append((vitri[0] + 1, vitri[1] - 1))
        elif (vitri[0] - 1, vitri[1] - 1) in viTriTrang:
            moveList.append((vitri[0] - 1, vitri[1] - 1))
    return moveList
    
def getMoveRook(vitri, luot):
    diemden = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    movesList = []
    ally = viTriTrang if luot == 'T' else viTriDen
    enemy = viTriDen if luot == 'T' else viTriTrang
    
    for d in diemden:
        for i in range(1, 8):
            end_row = vitri[0] + d[0] * i
            end_col = vitri[1] + d[1] * i
            
            
    
def getMoveKnight(vitri, luot):
    diemden = [(2, 1), (1, 2), (-2, 1), (-1, 2), (2, -1), (1, -2), (-2, -1), (-1, -2)] # di chuyen hinh chu L
    movesList = []
    ally = viTriTrang if luot == 'T' else viTriDen
    enemy = viTriDen if luot == 'T' else viTriTrang
    for d in diemden:
        end_row = vitri[0] + d[0]
        end_col = vitri[1] + d[1]
        if 0 <= end_row <= 7 and 0 <= end_col <= 7 and (end_row, end_col) not in ally:
                movesList.append((end_row, end_col))
    return movesList

def getMoveBishop(vitri, luot):
    diemden = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    movesList = []
    ally = viTriTrang if luot == 'T' else viTriDen
    enemy = viTriDen if luot == 'T' else viTriTrang
    for d in diemden:
        for i in range(1, 8):
            end_row = vitri[0] + d[0] * i
            end_col = vitri[1] + d[1] * i
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                if (end_row, end_col) in ally:
                    break
                elif (end_row, end_col) in enemy:
                    movesList.append((end_row, end_col))
                    break
                else:
                    movesList.append((end_row, end_col))
    return movesList

def getMoveQueen(vitri, luot):
    firstMoves = getMoveRook(vitri, luot)
    secondMoves = getMoveBishop(vitri, luot)
    moveList = firstMoves + secondMoves
    return moveList

def getMoveKing(vitri, luot):
    movesList = []
    diemDen = [(1, 1), (1, -1), (-1, 1), (-1, -1), (-1, 0), (1, 0), (0, -1), (0, 1)]
    ally = viTriTrang if luot == 'T' else viTriDen
    enemy = viTriDen if luot == 'T' else viTriTrang
    
    for d in diemDen:
        end_row = vitri[0] + d[0]
        end_col = vitri[1] + d[1]
        if (end_row, end_col) in ally and 0 <= end_col <= 7 and 0 <= end_row <= 7:
            movesList.append((end_row, end_col))
    return movesList
        
        
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
    
