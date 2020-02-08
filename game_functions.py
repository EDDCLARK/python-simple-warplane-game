import sys
import pygame
from Bullet import Bullet
from Alien import Alien
from time import sleep

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    '''响应按键'''
    if event.key==pygame.K_RIGHT:
        ship.moving_right=True #允许向右移动飞船
    elif event.key==pygame.K_LEFT:
        ship.moving_left=True #允许向左移动飞船
    elif event.key==pygame.K_UP:
        ship.moving_up=True #允许向上移动飞船
    elif event.key==pygame.K_DOWN:
        ship.moving_down=True #允许向下移动飞船
    elif event.key==pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)#按空格键调用fire_bullet()方法发射子弹
    elif event.key==pygame.K_ESCAPE:
        sys.exit() #按快捷键esc退出游戏 

def check_keyup_events(event,ship):
    '''响应松开按键'''
    if event.key==pygame.K_RIGHT:
        ship.moving_right=False
    elif event.key==pygame.K_LEFT:
        ship.moving_left=False
    elif event.key==pygame.K_UP:
        ship.moving_up=False
    elif event.key==pygame.K_DOWN:
        ship.moving_down=False      

def check_event(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    '''响应按键和鼠标事件'''
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)             
        elif event.type==pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button,mouse_x,mouse_y):
    '''在玩家单击按钮时开始游戏'''
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active=True
        #重置记分牌图像
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_score()
        sb.prep_ship()
        #清空外星人和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群新外星人，并让飞船回到初始位置
        create_fleet(ai_settings,screen,ship,aliens)
        ship.init_ship()

            

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    '''变更屏幕上的图像，并切换到新屏幕'''
    #每次循环都重绘屏幕更改颜色
    screen.fill(ai_settings.bg_color)
    #在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    #显示一个记分牌
    sb.show_score()
    #处于非游戏状态就绘制PLAY按钮
    if not stats.game_active:
        play_button.draw_button()
     #让最近绘制的一个屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,bullets,aliens):
    '''更新子弹位置并删除已消失在屏幕上的子弹'''
    #更新子弹位置
    bullets.update()
    #删除已消失在视线内的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom<=0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)


def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    '''响应子弹和外星人的碰撞'''
    #如果击中则将{子弹：外星人}一起删除
    collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        for aliens in collisions.values():
            stats.score+=ai_settings.alien_point*len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)
   #外星人被消灭完后，将子弹清空并生成一批新的外星人
    if len(aliens)==0:
        #删除现有子弹，加快游戏节奏
        bullets.empty()
        ai_settings.increase_speed()
        #整群外星人消灭就提高一个等级
        stats.level+=1
        sb.prep_level()
        create_fleet(ai_settings,screen,ship,aliens)    

def fire_bullet(ai_settings,screen,ship,bullets):
    '''子弹数量没达到上限就发射子弹'''
    #创建一个子弹，并把它加入到编组bullets中
    if len(bullets)<ai_settings.bullet_alowed:
        new_bullet=Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)
 


def create_fleet(ai_settings,screen,ship,aliens):
    '''创建外星人群'''
    #创建一个外星人，并计算一行可以容纳多少个外星人
    #外星人间距为外星人宽度
    alien=Alien(ai_settings,screen)
    number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    #创建外星人群
    for row_number in range(number_rows):
        #创建第一行外星人
        for alien_number in range(number_aliens_x):
            #创建一个外星人并把它加入当前行
            create_alien(ai_settings,screen,aliens,alien_number,row_number)

def get_number_aliens_x(ai_settings,alien_width):
    '''计算一行可以容纳多少个外星人'''
    available_space_x=ai_settings.screen_width-2*alien_width #去除边界后，剩余的可以用来显示外星人的宽度
    number_aliens_x=int(available_space_x/(alien_width*2)) #算上间距后 一行能显示的外星人数量
    return number_aliens_x
    
def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    '''创建一个外星人并放入当前行'''
    alien=Alien(ai_settings,screen)
    alien_width=alien.rect.width
    alien.x=alien_width+2*alien_width*alien_number
    alien.rect.x=alien.x
    alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)

def get_number_rows(ai_settings,ship_height,alien_height):
    '''计算屏幕上可以容纳多少行'''
    available_space_y=ai_settings.screen_height-(3*alien_height)-ship_height
    number_rows=int(available_space_y/(2*alien_height))
    return number_rows

def update_aliens(ai_settings,aliens,ship,stats,sb,screen,bullets):
    '''检查是否有外星人在边缘，并更新整群外星人的位置'''
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
    #检查有没有外星人到达屏幕底部
    check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets)

def check_fleet_edges(ai_settings,aliens):
    '''外星人到达边缘时采取的措施'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break
    
def change_fleet_direction(ai_settings,aliens):
    '''将整群外星人往下移，并改变移动方向'''
    for alien in aliens.sprites():
        alien.rect.y+=ai_settings.fleet_drop_speed
    ai_settings.fleet_direction*=-1

def ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets):
    '''响应被外星人撞到的飞船'''
    if stats.ship_left>0:
        #将ship_left减1
        stats.ship_left-=1
        #更新记分牌
        sb.prep_ship()
        #清空外星人列表和子弹列表
        bullets.empty()
        aliens.empty()
        #创建一群新的外星人，并将飞船置于初始位置
        create_fleet(ai_settings,screen,ship,aliens)
        ship.init_ship()
        #暂停几秒
        sleep(0.5)
    else:
        stats.game_active=False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets):
    '''检查是否有外星人到达了屏幕底部'''
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
            break

def check_high_score(stats,sb):
    '''检查是否诞生了最高得分'''
    if stats.score>stats.high_score:
        stats.high_score=stats.score
        sb.prep_high_score()




