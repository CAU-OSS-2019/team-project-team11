# 윷놀이 이동 위치 이벤트

import random



# 윷 이벤트 결과
def yutObject(player_id, numOfHorse, yutExecute=True): # 윷 던지고 난 결과     # 플레이어id, 말번호,  윷을 던지는 신호를 줄 경우

    dic = {'도': 1, '개': 2, '걸': 3, '윷': 4, '모': 5, '빽도': -1}

    n = random.sample(['도', '개', '걸', '윷', '모', '빽도'], 1)

    a = n[0]
    print(a)

    return player_id, numOfHorse, dic[a], n[0]


# 플레이어 말 초기 위치

class Horse:
    def __init__(self):
        self.posX = 6
        self.posY = -1

horse = Horse()
#print(horse.posX, horse.posY)


# main
# 지도 맵
N = 6
map = [[0 for col in range(N + 2)] for row in range(N + 2)]



# 윷 던지고 나서 이벤트 -> 일단은 말 하나만!!

# 다른 위치일 경우

# 플레이어, 몇번재의 말
'''
player_id = 2
numOfHorse = 1
print("플레이어 : ", player_id)
print("몇번째의 말 : ", numOfHorse)

# 현재위치
horse.posX, horse.posY = (4,4)
print("현재 위치 : ", horse.posX, horse.posY)

# 윷 던지고 난 결과
yut_result = yutObject(player_id, numOfHorse, True)[2]
print("윷 결과 : ", yut_result)
'''

before_x = [0,0,0,0,0,0]
before_y = [0,0,0,0,0,0]


# 입력값 : 플레이어 id, 해당 플레이어의 몇번째의 말, 말 전 위치 x값, 말 전 위치 y값, 현재 말 위치 x값, 현재 말 위치 y값

def yut_move(id, num, bx, by, x, y, z):
    player_id = id
    numOfHorse = num

    before_x = bx
    before_y = by
    # before_x[0]=0
    # before_y[0]=0

    if(z == -1): # 빽도일 경우
        if((horse.posX, horse.posY) == (6,-1)):
            return
        elif((horse.posX, horse.posY) == (6,1)):
            horse.posX = 6
            horse.posY = 0
            return player_id, numOfHorse, before_x, before_y, horse.posX, horse.posY
        else:
            horse.posX =  before_x[1]
            horse.posY =  before_y[1]
            before_x[1] = before_x[2]
            before_y[1] = before_y[2]
            return player_id, numOfHorse, before_x, before_y, horse.posX, horse.posY



    # 만약 시작점이 (6,-1)이라면
    if((horse.posX, horse.posY) == (6,-1)):
        horse.posX = 6
        horse.posY = 0
        yut_result = z
        while(yut_result):
            horse.posY += 1
            before_x[yut_result] = horse.posX
            before_y[yut_result] = horse.posY
            if ((horse.posX, horse.posY) == (6, 3)):  # (3,0) 예외처리하기
                horse.posY += 1
            yut_result -= 1
        return player_id, numOfHorse, before_x, before_y, horse.posX, horse.posY
    elif((horse.posX, horse.posY) == (6,0)): # 현재 위치가 (6,0)이라면
        print("도착")
        return player_id, numOfHorse
    else:
        horse.posX = x
        horse.posY = y
        yut_result = z

# 현재 위치가 (6,6)일경우
    if((horse.posX, horse.posY) == (6,6)):
        while(yut_result): #결과 칸수 -> 한칸씩 어떻게 변화를 하는지 알려줌
                before_x[yut_result] = horse.posX
                before_y[yut_result] = horse.posY
                if(horse.posX == 0 and horse.posY == 0):
                    horse.posX += 1
                else:
                    horse.posX -= 1
                    horse.posY -= 1
                yut_result -= 1
        return player_id, numOfHorse, before_x, before_y, horse.posX, horse.posY

# 현재 위치가 (0, 6)일 경우
    #if(horse.posX, horse.posY == (0,6)):
    if((horse.posX, horse.posY) == (0, 6)):
        while(yut_result): #-- & 현재위치가 아닐경우
                if(horse.posX > 6 and horse.posY> 0):
                    print("도착2!!")
                    break
                else:
                    before_x[yut_result] = horse.posX
                    before_y[yut_result] = horse.posY
                    horse.posX+=1
                    horse.posY-=1
                yut_result -= 1
        return player_id, numOfHorse, before_x, before_y, horse.posX, horse.posY


# 현재 위치가 (3, 3)일 경우
    if((horse.posX, horse.posY) == (3,3)):
        while(yut_result):# -- & 현재위치가 아닐경우):
                if(horse.posX >= 6 and horse.posY <= 0):
                    print("도착3!!")
                    break
                else:
                    before_x[yut_result] = horse.posX
                    before_y[yut_result] = horse.posY
                    horse.posX+=1
                    horse.posY-=1
                yut_result -= 1
        return player_id, numOfHorse,  before_x, before_y, horse.posX, horse.posY

# 안에
# 현재 위치가 대각선이라면...(3, 3) (6,6), (0,6)을 제외한
# (1, 1), (2, 2), (4, 4), (5, 5), (1, 5), (2, 4), (4, 2), (5, 1)
    if(((horse.posX, horse.posY) == (1, 1)) or ((horse.posX, horse.posY) == (2, 2)) or ((horse.posX, horse.posY) == (4, 4)) or ((horse.posX, horse.posY) == (5, 5)) or ((horse.posX, horse.posY) == (1, 5)) or ((horse.posX, horse.posY) == (2, 4)) or ((horse.posX, horse.posY) == (4, 2)) or ((horse.posX, horse.posY) == (5, 1))):
        while(yut_result):# -- & 현재위치가 아닐경우):
            if((horse.posX, horse.posY) == (0, 0)):
                before_x[yut_result] = horse.posX
                before_y[yut_result] = horse.posY
                horse.posX += 1
            elif(((horse.posX, horse.posY) == (1, 5)) or ((horse.posX, horse.posY) == (2, 4)) or ((horse.posX, horse.posY) == (4, 2)) or ((horse.posX, horse.posY) == (5, 1))):# y=-2x꼴
                if((horse.posX, horse.posY) == (2, 4) and (yut_result > 1)):
                    if(yut_result == 2):
                        while(yut_result):
                            before_x[yut_result] = horse.posX
                            before_y[yut_result] = horse.posY
                            horse.posX = horse.posX + 1
                            horse.posY = horse.posY - 1
                            yut_result-=1
                        #horse.posX += 2
                        #horse.posY -= 2
                        break
                    elif(yut_result == 3):
                        while (yut_result):
                            before_x[yut_result] = horse.posX
                            before_y[yut_result] = horse.posY
                            horse.posX = horse.posX + 1
                            horse.posY = horse.posY - 1
                            yut_result -= 1
                        #horse.posX += 3
                        #horse.posY -= 3
                        break
                    elif(yut_result == 4):
                        while (yut_result):
                            before_x[yut_result] = horse.posX
                            before_y[yut_result] = horse.posY
                            horse.posX = horse.posX + 1
                            horse.posY = horse.posY - 1
                            yut_result -= 1
                        #horse.posX += 4
                        #horse.posY -= 4
                        break
                    elif(yut_result == 5):
                        print("도착!!")
                        break
                before_x[yut_result] = horse.posX
                before_y[yut_result] = horse.posY
                horse.posX+=1
                horse.posY-=1
            elif(horse.posX == horse.posY):  # y=2x꼴
                before_x[yut_result] = horse.posX
                before_y[yut_result] = horse.posY
                horse.posX -= 1
                horse.posY -= 1
            else:
                before_x[yut_result] = horse.posX
                before_y[yut_result] = horse.posY
                horse.posX += 1
                if ((horse.posX, horse.posY) == (3, 0)): # (3,0) 예외처리하기
                    horse.posX += 1
            if(horse.posX > 6 and horse.posY <= 0):
                print("도착4!!")
                break
            yut_result -= 1
        return player_id, numOfHorse, before_x, before_y , horse.posX, horse.posY

# 현재위치가 대각선, (6,6), (0,6), (3,3)이 아니라면
    while(yut_result):
        if(horse.posX == 6 and ((horse.posY < 6) and (horse.posY > 0))):  # 현재 위치가 어디에 있는지
            before_x[yut_result] = horse.posX
            before_y[yut_result] = horse.posY
            horse.posY+=1
            if ((horse.posX, horse.posY) == (6, 3)):  # (3,0) 예외처리하기
                horse.posY += 1
        elif(((horse.posX > 0) and (horse.posX <= 6)) and horse.posY == 6):
            before_x[yut_result] = horse.posX
            before_y[yut_result] = horse.posY
            horse.posX-=1
            if ((horse.posX, horse.posY) == (3, 6)):  # (3,0) 예외처리하기
                horse.posX -= 1
        elif((horse.posX, horse.posY) == (0, 0)):
            before_x[yut_result] = horse.posX
            before_y[yut_result] = horse.posY
            horse.posX += 1
        elif(horse.posX == 0 and ((horse.posY <= 6) and (horse.posY > 0))):
            before_x[yut_result] = horse.posX
            before_y[yut_result] = horse.posY
            horse.posY-=1
            if ((horse.posX, horse.posY) == (0, 3)):  # (3,0) 예외처리하기
                horse.posY -= 1
        elif(horse.posX <= 6 and horse.posY == 0):
            before_x[yut_result] = horse.posX
            before_y[yut_result] = horse.posY
            horse.posX+=1
            if ((horse.posX, horse.posY) == (3, 0)):  # (3,0) 예외처리하기
                horse.posX += 1
        if(horse.posX > 6 and horse.posY == 0):
            print("도착5!!")
            break
        yut_result -= 1
    return player_id, numOfHorse, before_x, before_y, horse.posX, horse.posY

# 반환값 : 플레이어 id, 해당 플레이어의 몇번째의 말, 말 전 위치 x값, 말 전 위치 y값, 현재 말 위치 x값, 현재 말 위치 y값


'''
# test용

print(yut_move(player_id, numOfHorse, before_x, before_y, horse.posX, horse.posY, yut_result))

# 현재위치

print("현재 위치 : ", horse.posX, horse.posY)


# 윷 던지고 난 결과
yut_result = yutObject(player_id, numOfHorse, True)[2]
print("윷 결과 : ", yut_result)
print(yut_move(player_id, numOfHorse, before_x, before_y, horse.posX, horse.posY, yut_result))
'''


# 다음 계획
# - 인터페이스
# - 말 잡을때
# - 낙
# - 전체 틀

