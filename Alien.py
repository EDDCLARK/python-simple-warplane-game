import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''表示单个外星人的类'''
    def __init__(self,ai_settings,screen):
        '''初始化外星人并设置其起始位置'''
        super().__init__()
        self.screen=screen
        self.ai_settings=ai_settings

        #加载外星人图像并设置其rect属性
        import_image=pygame.image.load(r'C:\Users\11526\Desktop\python work\.vscode\alien_invasion\images\萌版航空航天-外星人飞船alien-co.png')
        self.image=pygame.transform.scale(import_image,(80,60))#对导入的图片进行缩放
        self.rect=self.image.get_rect()

        #每个外星人最初都在左上角
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height

        #储存外星人的准确位置
        self.x=float(self.rect.x)

    def blitme(self):
        '''在指定位置绘制外星人'''
        self.screen.blit(self.image,self.rect)

    def update(self):
        '''向左或向右移动外星人'''
        self.x+=self.ai_settings.alien_speed_factor*self.ai_settings.fleet_direction
        self.rect.x=self.x

    def check_edges(self):
        '''如果外星人处于屏幕边界则返回TRUE'''
        screen_rect=self.screen.get_rect()
        if self.rect.right>=screen_rect.right:
            return True
        elif self.rect.left<=0:
            return True


