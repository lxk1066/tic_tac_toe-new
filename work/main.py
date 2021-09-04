# tic_tac_toe
# -*- coding:UTF-8 -*-
import tkinter.messagebox
import pygame
import time
from tkinter import *
from tkinter.messagebox import *
from Class import Player
Tk().wm_withdraw()


# 判断先后手
def judge_sequence():
    if play_o.get_initiative():
        return 1
    elif play_x.get_initiative():
        return 2


# 判断是否平局
# 遍历数组，如果发现-1就说明棋盘上还有空位没下棋子
def judge_dogfall():
    for i in board:
        for j in i:
            if j == -1:
                return False
    return True


# 判断谁是winner
def judge_winner():
    if play_o.get_status():
        return "player_o"
    elif play_x.get_status():
        return "player_x"


# 判断谁是loser
def judge_loser():
    if play_o.get_status() is None:
        return None
    if not play_o.get_status():
        return "player_o"
    elif not play_x.get_status():
        return "player_x"


# 保存对局记录
def save_result():
    localtime = time.asctime(time.localtime(time.time()))
    with open('save_result.txt', 'a+', encoding='utf-8') as f:
        f.write("{}\n".format(localtime))
        f.write("胜方: {}\n负方: {}\n".format(judge_winner(), judge_loser()))
        f.write("对局棋谱: \n")
        for i in board:
            for j in i:
                if j == -1:
                    f.write("■\t")
                elif j == 1:
                    f.write("o\t")
                else:
                    f.write("x\t")
            f.write("\n")
        f.write("\n")


# 根据鼠标所在位置坐标返回第几个格子
def position(mouse_post):
    post_x, post_y = mouse_post[0], mouse_post[1]
    if 0 < post_x < 200 and 0 < post_y < 200:
        return 1
    elif 200 < post_x < 400 and 0 < post_y < 200:
        return 2
    elif 400 < post_x < 600 and 0 < post_y < 200:
        return 3
    elif 0 < post_x <= 200 and 200 < post_y <= 400:
        return 4
    elif 200 < post_x < 400 and 200 < post_y <= 400:
        return 5
    elif 400 < post_x < 600 and 200 < post_y < 400:
        return 6
    elif 0 < post_x < 200 and 400 < post_y < 600:
        return 7
    elif 200 < post_x < 400 and 400 < post_y < 600:
        return 8
    elif 400 < post_x < 600 and 400 < post_y < 600:
        return 9


# 根据position()返回值计算出在二维数组board中的对应位置并判断是否可以下(棋)子
def judge_board(mouse_now, *args):
    position_num = position(mouse_now)
    a = int((position_num - 1) / 3)
    b = (position_num - 1) % 3
    if len(args) != 0:
        board[a][b] = args[0]
    return True if board[a][b] == -1 else False


# 返回所在格子的四个顶点坐标，顺序为上、右、下、左
def getx_gety(mouse_post):
    posts = []
    numbers = {
        1: [0, 0],
        2: [200, 0],
        3: [400, 0],
        4: [0, 200],
        5: [200, 200],
        6: [400, 200],
        7: [0, 400],
        8: [200, 400],
        9: [400, 400]
    }

    num = position(mouse_post)

    port = numbers.get(num, None)
    posts.append(port)
    posts.append([port[0]+200, port[1]])
    posts.append([port[0]+200, port[1]+200])
    posts.append([port[0], port[1]+200])

    return posts


# 算出画叉的四个坐标,参数posts_fork来自getx_gety()函数的返回值
def fork_posts(posts_fork):
    fork_x = [posts_fork[0][0] + 60, posts_fork[0][1] + 60]
    fork_y = [posts_fork[2][0] - 60, posts_fork[2][1] - 60]
    fork_j = [posts_fork[1][0] - 60, posts_fork[1][1] + 60]
    fork_k = [posts_fork[3][0] + 60, posts_fork[3][1] - 60]
    return [fork_x, fork_y, fork_j, fork_k]


# 算出画圆的圆心坐标，参数post_circle来自getx_gety()函数的返回值
# 在正方形内画圆，圆心坐标计算公式为((x1+x2+x3+x4)/4,(y1+y2+y3+y4)/4)
def circle_post(post_circle):
    post_x, post_y = 0, 0
    for q in post_circle:
        post_x += q[0]
        post_y += q[1]
    pos = [post_x / 4, post_y / 4]
    return pos


# ----------------------------------------逻辑部分------------------------------------------------
# 判断结果
def compute():
    i = 0
    result = -1
    # 检查行
    while (result == -1) and (i < size):
        num_of_x, num_of_o = 0, 0
        j = 0
        while j < size:
            if board[i][j] == 1:
                num_of_x += 1
            elif board[i][j] == 0:
                num_of_o += 1
            if num_of_o == size:
                result = 0
            elif num_of_x == size:
                result = 1
            j += 1
        i += 1
    # 检查列
    if result == -1:
        i, j = 0, 0
        while j < size and result == -1:
            num_of_x = num_of_o = 0
            i = 0
            while i < size:
                if board[i][j] == 1:
                    num_of_x += 1
                elif board[i][j] == 0:
                    num_of_o += 1
                if num_of_o == size:
                    result = 0
                elif num_of_x == size:
                    result = 1
                i += 1
            j += 1
    # 检查正对角线
    if result == -1:
        num_of_o = num_of_x = 0
        i, j = 0, 0
        while i < size:
            if board[i][i] == 1:
                num_of_x += 1
            elif board[i][i] == 0:
                num_of_o += 1
            if num_of_o == size:
                result = 0
            elif num_of_x == size:
                result = 1
            i += 1
    # 检查斜对角线
    if result == -1:
        num_of_o = num_of_x = 0
        i, j = 0, 0
        while i < size:
            if board[i][size-i-1] == 1:
                num_of_x += 1
            elif board[i][size-i-1] == 0:
                num_of_o += 1
            if num_of_o == size:
                result = 0
            elif num_of_x == size:
                result = 1
            i += 1
    return result


# ---------------------------------------GUI图形部分------------------------------------------
# 画图
def paint_circle(mouse_now):
    if position(mouse_now) % 2 == 0:
        color = white
    else:
        color = black
    post = getx_gety(mouse_now)
    pygame.draw.circle(screen, color, circle_post(post), 50, 3)


def paint_fork(mouse_now):
    if position(mouse_now) % 2 == 0:
        color = white
    else:
        color = black
    post = fork_posts(getx_gety(mouse_now))
    pygame.draw.line(screen, color, post[0], post[1], 3)
    pygame.draw.line(screen, color, post[2], post[3], 3)


# 提示先后手的那两个圆
def paint_circle_first():
    pygame.draw.circle(screen, black, [625, 60], 20, 0)


def paint_circle_next():
    pygame.draw.circle(screen, black, [625, 145], 20, 0)


def paint_game_records():
    pygame.draw.rect(screen, my_blue, (600, 0, 50, 200), 0)
    screen.blit(text9, (610, 10))
    screen.blit(text10, (610, 55))
    screen.blit(text11, (610, 100))
    screen.blit(text12, (610, 150))


# 刷新背景
def background():
    screen.fill([199, 193, 245])
    pygame.draw.rect(screen, white, [0, 0, 200, 200], 0)
    pygame.draw.rect(screen, black, [200, 0, 200, 200], 0)
    pygame.draw.rect(screen, white, [400, 0, 200, 200], 0)
    pygame.draw.rect(screen, black, [0, 200, 200, 200], 0)
    pygame.draw.rect(screen, white, [200, 200, 200, 200], 0)
    pygame.draw.rect(screen, black, [400, 200, 200, 200], 0)
    pygame.draw.rect(screen, white, [0, 400, 200, 200], 0)
    pygame.draw.rect(screen, black, [200, 400, 200, 200], 0)
    pygame.draw.rect(screen, white, [400, 400, 200, 200], 0)
    pygame.draw.lines(screen, lightgrey, True, [(600, 0), (650, 0), (650, 200), (600, 200)], 3)
    pygame.draw.lines(screen, lightgrey, True, [(600, 200), (650, 200), (650, 400), (600, 400)], 3)
    pygame.draw.lines(screen, lightgrey, True, [(600, 400), (650, 400), (650, 600), (600, 600)], 3)
    pygame.draw.circle(screen, black, [625, 145], 20, 3)
    pygame.draw.circle(screen, black, [625, 60], 20, 3)
    screen.blit(text1, (610, 225))
    screen.blit(text2, (610, 262))
    screen.blit(text3, (610, 299))
    screen.blit(text4, (609, 336))
    screen.blit(text5, (610, 3))
    screen.blit(text6, (610, 85))
    pygame.display.update()


while True:
    # 主程序
    size = 3
    n = 0        # 判断游戏是否结束的全局变量
    board = []
    white = [255, 255, 255]
    black = [0, 0, 0]
    bright_green = (0, 255, 0)
    lightgrey = [125, 125, 125]
    my_blue = [199, 193, 245]

    for k in range(3):
        board.append([])
        for h in range(3):
            board[k].append(-1)

    pygame.init()
    pygame.display.init()
    screen = pygame.display.set_mode([650, 600])
    pygame.display.set_caption("tic_tac_toe")
    my_font = pygame.font.Font("fzlt.ttf", 30)
    text1 = my_font.render("重", True, black)
    text2 = my_font.render("新", True, black)
    text3 = my_font.render("开", True, black)
    text4 = my_font.render("始", True, black)
    text5 = my_font.render("O", True, black)
    text6 = my_font.render("X", True, black)
    text7 = my_font.render("只要心中有梦想的火种，", True, black)
    text8 = my_font.render("终于一天我们会被生活点燃！", True, black)
    text9 = my_font.render("对", True, black)
    text10 = my_font.render("局", True, black)
    text11 = my_font.render("记", True, black)
    text12 = my_font.render("录", True, black)
    # 刷新背景
    background()

    # 让用户选择是O为先手还是X为先手
    if tkinter.messagebox.askyesno("提示", "请选择先手是画O(Y)或者画X(N)？\n      其中O为左击，X为右击"):
        initiative = 1
    else:
        initiative = 0

    if initiative:
        play_o = Player(True)
        play_x = Player(False)
    else:
        play_o = Player(False)
        play_x = Player(True)

    while True:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()

            # 通过判断先后手来更新右上角的提示
            if judge_sequence() == 1 and n == 0:
                paint_circle_first()
                pygame.draw.circle(screen, [199, 193, 245], [625, 145], 17, 0)
            elif judge_sequence() == 2 and n == 0:
                paint_circle_next()
                pygame.draw.circle(screen, [199, 193, 245], [625, 60], 17, 0)
            pygame.display.update()

            # 鼠标悬停重新开始时高亮
            if 600 <= mouse[0] <= 650 and 200 <= mouse[1] <= 400:
                pygame.draw.lines(screen, [72, 246, 31], True, [(600, 200), (650, 200), (650, 400), (600, 400)], 3)
            else:
                pygame.draw.lines(screen, lightgrey, True, [(600, 200), (650, 200), (650, 400), (600, 400)], 3)
            pygame.display.update()

            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 鼠标的x坐标
                x = event.pos[0]
                # 鼠标的y坐标
                y = event.pos[1]

                # 点击重新开始按钮
                if 600 <= mouse[0] <= 650 and 200 <= mouse[1] <= 400 and event.button == 1:
                    n = 1

                # 隐藏彩蛋，显示一句话
                if 650 >= mouse[0] >= 600 >= mouse[1] >= 400 and event.button == 1:
                    n = 3    # 更改控制变量，防止paint_game_records()函数执行
                    screen.fill([255, 255, 255])
                    screen.blit(text7, (180, 200))
                    screen.blit(text8, (150, 250))
                pygame.display.update()

                # 通过鼠标坐标和其他条件来判断下(棋)子
                if n == 0:
                    if judge_board(mouse):
                        if event.button == 1 and judge_sequence() == 1:
                            paint_circle(mouse)
                            judge_board(mouse, 1)
                            pygame.display.update()
                            play_o.update()
                            play_x.update()
                        elif event.button == 3 and judge_sequence() == 2:
                            paint_fork(mouse)
                            judge_board(mouse, 0)
                            pygame.display.update()
                            play_o.update()
                            play_x.update()

                if n == 0:
                    if compute() == 1:
                        showinfo("提示", "O WIN!")
                        play_o.set_winner()
                        play_x.set_loser()
                        n = 2
                    elif compute() == 0:
                        showinfo("提示", "X WIN!")
                        play_x.set_winner()
                        play_o.set_loser()
                        n = 2
                    elif judge_dogfall() and compute() == -1:
                        showinfo("提示", "平局！")
                        n = 2

                if n == 2:
                    paint_game_records()
                    save_result()

        # 重新开始
        if n == 1:
            break
