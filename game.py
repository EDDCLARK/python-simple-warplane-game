import sys
import pygame
from  pygame.sprite import Group
from Alien import Alien
from settings import Settings
from ship import Ship
from game_stats import GameStats
import game_functions as gf
from button import Button
from scoreboard import Scoreboard

'''创建pygame窗口以及响应用户输入'''
def run_game():
    #初始化pygame、设置和屏幕对象
    pygame.init()
    ai_settings=Settings()
    screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))   #调用类属性创建宽1200像素，高800像素的窗口界面
    pygame.display.set_caption("Allien Invasion")   #窗口标题命名
    #创建一个用于存储统计信息的实例
    stats=GameStats(ai_settings)
    #创建一个记分牌
    sb=Scoreboard(ai_settings,screen,stats)
    #创建play按钮
    play_button=Button(ai_settings,screen,"PLAY")
    #创建一艘飞船
    ship=Ship(ai_settings,screen)
    #创建一个用于存储子弹的编组
    bullets=Group()
    #创建一个用于存储外星人的编组
    aliens=Group()
    #创建外星人群
    gf.create_fleet(ai_settings,screen,ship,aliens)

    #开始游戏的主循环
    while True:
        #监视键盘和鼠标事件
        gf.check_event(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,bullets,aliens)
            gf.update_aliens(ai_settings,aliens,ship,stats,sb,screen,bullets)
        
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)
        

        
run_game()
