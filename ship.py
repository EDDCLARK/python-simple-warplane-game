import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self,ai_settings,screen):
        '''初始化飞船，并设置其初始位置'''
        super(Ship,self).__init__()
        self.ai_settings=ai_settings
        self.screen=screen
        #加载飞船图像并获取其外接矩形
        import_image=pygame.image.load(r'C:\Users\11526\Desktop\python work\.vscode\alien_invasion\images\航空航天-隐形飞机飞船.png')
        self.image=pygame.transform.scale(import_image,(80,60)) #对导入的图片进行缩放
        self.rect=self.image.get_rect()
        self.screen_rect=screen.get_rect()
        #将每艘飞船放在屏幕底部中央
        self.rect.centerx=self.screen_rect.centerx
        self.rect.bottom=self.screen_rect.bottom
        #在飞船的属性center和row中存储小数值
        self.center=float(self.rect.centerx)
        self.row=float(self.rect.centery)
        self.moving_right=False  #初始的移动标志，控制是否要向右移动
        self.moving_left=False   #初始的移动标志，控制是否向左移动
        self.moving_up=False #初始的移动标志，控制是否向上移动
        self.moving_down=False #初始的移动标志，控制是否向下移动
    
    def blitme(self):
        '''在指定位置绘制飞船'''
        self.screen.blit(self.image,self.rect)

    def update(self):
        '''根据移动标志调整飞船的位置'''
        #更新center值而不是rect以实现非整数的移动
        if self.moving_right and self.rect.right<self.screen_rect.right: #避免从右边出界
            self.center+=self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left>0: #避免从左边出界
            self.center-=self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top>0:
            self.row-=self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom<self.screen_rect.bottom:
            self.row+=self.ai_settings.ship_speed_factor

        #根据center值更新rect对象
        self.rect.centerx=self.center
        self.rect.centery=self.row

    def init_ship(self):
        '''使飞船回到初始位置'''
        #假定飞船不进行上下移动
        self.center=self.screen_rect.centerx
        
        
        

        
