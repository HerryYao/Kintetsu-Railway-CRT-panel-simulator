# Japanese train info UI simulator by Herry, requires pygame module
# installation 'pip install pygame'

from sys import exit
from time import sleep
import pygame
import random

"""
try:
  print(random.randint(2,6))
except:
  exit()
"""
# train info load
stations = open("stations.txt", "r", encoding="utf-8")
TRstation = []
for x in stations:
    TRstation.append(x)
def renew_station():
    ThisStation = TRstation[random.randint(1,len(TRstation)-1)] # txt starts at 1
    # 2 or 4 of ParentTab should be the actual parent location
    seq = [2,4]
    global ParentTab, ChildTab, RomanjiTab
    seqq = random.choice(seq)
    ParentTab = ThisStation.split(";")[seqq]
    ChildTab = ThisStation.split(";")[seqq+1][:-1]
    if seqq == 2:
        RomanjiTab = ThisStation.split(";")[seqq+4][:-1]
    else:
        RomanjiTab = ThisStation.split(";")[seqq+3][:-1]

# track & train load
def track():
    return str(random.randint(1,8))
Box_High_Surface = pygame.image.load("box_high.png")
Box_Low_Surface = pygame.image.load("box_low.png")
Box_High_Colors = ["box_high_blue.png","box_high_gray.png","box_high_red.png"]
Box_Low_Colors = ["box_low_blue.png","box_low_gray.png","box_low_red.png"]

# display init
ScreenHeight = 600
FastH = ScreenHeight // 8
def if_red():
    return random.choice([(255,0,0),(255,255,255)])
def train_type():
    train_types = ["普通","普通","普通","普通","普通",
            "普通","急行","急行","急行","快特","終電"]
    return train_types[random.randint(0,len(train_types)-1)]
train_type_romanji = {
    "普通": "LOCAL",
    "急行": "EXPRESS",
    "快特": "LIM. EXPRESS",
    "終電": "END LINE"
}


# pygame init
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((800,ScreenHeight),pygame.FULLSCREEN)
pygame.display.set_caption("japan.railway.service")

# fonts
FONT = pygame.font.Font("MochiyPopOne-Regular.ttf", FastH)
Child_FONT = pygame.font.Font("MochiyPopOne-Regular.ttf", int(FastH*1.4))
Roma_FONT = pygame.font.Font("BestTen-DOT.otf", FastH)
Track_FONT = pygame.font.Font("Ubuntu-B.ttf", int(FastH*2.9))
time_FONT = pygame.font.Font("Ubuntu-B.ttf", int(FastH*1.5))
"""
    for n in range(1,4):
        while Settings[n] != table_Used[n][0][0]:
            wheel_T(n)
    if input("DECODE? [Y]").lower() == "y":
        DECODE = True
    else:
        DECODE = False
"""

while True:
    clock.tick(1)
    window.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == 27:
                pygame.quit()
                exit()
            # fetch first train
            renew_station()
            main_parent = FONT.render(
                ParentTab, False, (255,255,255)
            )
            main_parent = pygame.transform.scale(main_parent,(FastH*2,FastH))
            main_child = Child_FONT.render(
                ChildTab , False, (255,255,255)
            )
            main_romanji = Roma_FONT.render(
                RomanjiTab.upper(), False, (255,255,255)
            )
            main_track = Track_FONT.render(
                track(), False, (255,255,255)
            )
            i = if_red()
            main_sequence = FONT.render(
                "先発", False, (i)
            )
            sequence_romanji = Roma_FONT.render(
                "DEP.1st", False, (i)
            )
            alt_sequence = FONT.render(
                "次発", False, (0,255,0)
            )
            track_hiragana = FONT.render(
                "のりば", False, (255,255,255)
            )
            track_romanji = Roma_FONT.render(
                "TRACK", False, (255,255,255)
            )
            # whole time section for both trains
            time_table = [random.randint(0,23),random.randint(0,59)]
            i = ["",""]
            for x in time_table:
                if x - 10 < 0:
                    i[time_table.index(x)] = "0"
            main_time = time_FONT.render(
                f"{i[0] + str(time_table[0])}:{i[1] + str(time_table[1])}", False, (255,255,255)
            )
            i = [random.randint(0,1),random.randint(4,25)]
            time_table
            if time_table[0] + i[0] > 23:
                time_table[0] = (time_table[0] + i[0]) % 23
            else:
                time_table[0] = (time_table[0] + i[0])
            if time_table[1] + i[1] > 59:
                time_table[0] += 1
                if time_table[0] == 24:
                    time_table[0] = 0
                time_table[1] = (time_table[1] + i[1]) % 59
            else:
                time_table[1] = (time_table[1] + i[1])
            i = ["",""]
            for x in time_table:
                if x - 10 < 0:
                    i[time_table.index(x)] = "0"
            alt_time = time_FONT.render(
                f"{i[0] + str(time_table[0])}:{i[1] + str(time_table[1])}", False, (255,255,255)
            )
            # train types
            x = train_type()
            if x == "普通":
                y = Box_High_Colors[0]
            elif x == "急行" or x == "快特":
                y = Box_High_Colors[2]
            elif x == "終電":
                y = Box_High_Colors[1]
            main_train = Child_FONT.render(
                x, False, (255,255,255)
            )
            main_train_color = pygame.image.load(y)
            main_train_romanji = Roma_FONT.render(
                train_type_romanji[x], False, (255,255,255)
            )
            # alt train type
            x = train_type()
            if x == "普通":
                y = Box_Low_Colors[0]
            elif x == "急行" or x == "快特":
                y = Box_Low_Colors[2]
            elif x == "終電":
                y = Box_Low_Colors[1]
            alt_train = Child_FONT.render(
                x, False, (255,255,255)
            )
            alt_train_color = pygame.image.load(y)
            # if station name contains parent name
            # transform tool is to keep a fixed size surface
            if ParentTab == "":
                main_child = pygame.transform.scale(main_child,(FastH*5.2,FastH*3.5))
                main_parent = pygame.transform.scale(main_parent,(1,1))
                child_shrinked_width = FastH*3.45
            else:
                main_child = pygame.transform.scale(main_child,(FastH*4,FastH*3.5))
                main_parent = pygame.transform.scale(main_parent,(FastH*1.4,FastH*1.2))
                child_shrinked_width = FastH*4.7
            if len(RomanjiTab) > 7:
                main_romanji = pygame.transform.scale(main_romanji,(FastH*4.6,FastH*0.4))
                roma_width = FastH*3.7
            else:
                main_romanji = pygame.transform.scale(main_romanji,(FastH*2.8,FastH*0.4))
                roma_width = FastH*4.7
            main_train_romanji = pygame.transform.scale(main_train_romanji,(FastH*2.3,FastH*0.4))
            track_hiragana = pygame.transform.scale(track_hiragana,(FastH*1.9,FastH*1.3))
            track_romanji = pygame.transform.scale(track_romanji,(FastH*1.5,FastH*0.35))
            sequence_romanji = pygame.transform.scale(sequence_romanji,(FastH*1.5,FastH*0.2))
            # refresh secend train tab
            renew_station()
            alt_parent = FONT.render(
                ParentTab, False, (255,255,255)
            )
            alt_parent = pygame.transform.scale(alt_parent,(FastH*2,FastH))
            alt_child = Child_FONT.render(
                ChildTab , False, (255,255,255)
            )
            alt_romanji = Roma_FONT.render(
                RomanjiTab.upper(), False, (255,255,255)
            )
            alt_track = Track_FONT.render(
                track(), False, (255,255,255)
            )
            # transform for second train
            if ParentTab == "":
                alt_child = pygame.transform.scale(alt_child,(FastH*5.2,FastH*2.5))
                alt_parent = pygame.transform.scale(alt_parent,(1,1))
                alt_child_shrinked_width = FastH*3.4
            else:
                alt_child = pygame.transform.scale(alt_child,(FastH*4.5,FastH*2.5))
                alt_parent = pygame.transform.scale(alt_parent,(FastH,FastH*1.2))
                alt_child_shrinked_width = int(FastH*4.25)
            alt_track = pygame.transform.scale(alt_track,(FastH*1.6,FastH*2.6))
            # start to blit surfaces
            surfaces = [
                main_parent, 
                main_child,
                main_romanji,
                main_track,
                #
                alt_parent, 
                alt_child,
                alt_track,
                #
                main_sequence,
                sequence_romanji,
                alt_sequence,
                main_time,
                alt_time,
                track_hiragana,
                track_romanji,
                main_train_color, # sam place
                Box_High_Surface, # sam place
                alt_train_color,
                main_train,
                main_train_romanji,
                Box_Low_Surface,
                alt_train
            ]
            surface_loc = [
                (int(FastH*3.3),FastH*1.4),
                (child_shrinked_width,int(FastH*0.9)),
                (roma_width,int(FastH*4)),
                (int(FastH*8.9),int(FastH*1.3)),
                #
                (int(FastH*3.3),FastH*5.9),
                (alt_child_shrinked_width,int(FastH*5.6)),
                (int(FastH*8.9),int(FastH*5.6)),
                #
                (FastH*0.6,FastH*0.01),
                (FastH*0.9,FastH*1.26),
                (FastH*0.6,int(FastH*4.5)),
                (FastH*4,FastH*0.007), # main time
                (FastH*4,FastH*4.4), # alt time
                (FastH*8.65,FastH*0.007), # track
                (FastH*8.9,FastH*1.1), # track
                (FastH//7.5, FastH*1.5), # main train color
                (FastH//7.5, FastH*1.5), # box high
                (FastH//7.5, FastH*6),# alt train color
                (FastH*0.2, FastH*1.8), # main train
                (FastH*0.6, int(FastH*3.7)), # main tr roma
                (FastH//7.5, FastH*6), # box low
                (FastH*0.2, FastH*5.8)
            ]
            for x in surfaces:
                i = surfaces.index(x)
                window.blit(x,surface_loc[i])
                pygame.display.update()
                sleep(0.1)
