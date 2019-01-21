import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self,ai_settings,screen):
        super(Ship, self).__init__()
        '初始化飞船设置其初始位置'
        self.screen=screen
        self.ai_settings=ai_settings
        #加载飞船图像并获取其外接矩形
        self.image=pygame.image.load('images/1695710c-eda5-48ac-b77f-59620daa4632.png')
        self.rect=self.image.get_rect()
        self.screen_rect=screen.get_rect()
        #将每艘飞船放在屏幕底部中央
        self.rect.centerx=self.screen_rect.centerx
        self.rect.bottom=self.screen_rect.bottom

        #在飞船的属性center中存储小数值
        self.centerx=self.rect.centerx
        self.centery=self.rect.bottom
        #移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
    def update(self):
        '更具移动标志调整飞船的位置'
        #更新飞船的center值，而不是rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.ai_settings.ship_speed_factor
        if self.moving_up:
            self.centery -= self.ai_settings.ship_speed_factor
        if self.moving_down:
            self.centery += self.ai_settings.ship_speed_factor
        #根据self.center更新rect对象
        self.rect.centerx=self.centerx
        self.rect.bottom = self.centery

    def blitme(self):
        '在指定位置绘制飞船'
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.rect.centerx = self.screen_rect.centerx
        self.centerx=self.rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.centery=self.rect.bottom
