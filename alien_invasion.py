import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf

from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button

#tk窗口设置
import tkinter
from tkinter import messagebox
from multiprocessing import Process

#数据保存
import os

def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings=Settings()
    #创建游戏显示窗口
    screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption('外星人')
    #创建按钮
    play_button=Button(ai_settings,screen,"Play")
    #创建一个飞船，一个子弹编组和一个外星人编组
    ship=Ship(ai_settings,screen)
    #创建一个用于存储子弹的编组
    bullets=Group()
    bullets1 = Group()
    aliens=Group()
    # 创建一个用于存储游戏信息的实例
    stats=GameStats(ai_settings)
    # 创建存储游戏统计信息的实例，并创建记分牌
    sb = Scoreboard(ai_settings, screen, stats)
    #创建外星人群
    gf.create_fleet(ai_settings,screen,ship,aliens)
    #创建一个外星人
    # alien=Alien(ai_settings,screen)

    while True:
        #更新屏幕
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, bullets1, play_button)
        #监视键盘和鼠标事件
        gf.check_events(ai_settings,screen,stats,sb, play_button, ship,aliens,bullets,bullets1)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets,bullets1)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets,bullets1)

def func():
    if len(var.get())==0:
        tkinter.messagebox.showerror(title='错误！！',message='请填写玩家名称！！！！')
    else:
        p=Process(target=run_game)
        p.start()


if __name__ == '__main__':

    win=tkinter.Tk()
    win.title('游戏创建')
    win.geometry('300x200')

    lable=tkinter.Label(win,text='请输入游戏名称哟！！',anchor='center',font=('黑体',10))
    lable.place(x=50,y=50)
    var=tkinter.Variable()

    text=tkinter.Entry(win,textvariable=var)

    text.place(x=50, y=70)
    button=tkinter.Button(win,text='进入游戏',command=func)

    button.place(x=50,y=90)
    win.mainloop()
