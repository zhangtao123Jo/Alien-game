import pygame
from pygame.sprite import Sprite

class Bullet1(Sprite):
    '一个对飞船发射的子弹进行管理的类'
    def __init__(self,ai_settings,screen,ship):
        super(Bullet1,self).__init__()
        self.screen=screen

        #在（0.0）处创建一个表示子弹的矩形，在设置正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        # self.image=pygame.image.load('D:/学习资料/py/论文毕设/images/acc.png')

        self.rect.centerx=ship.rect.centerx+30
        self.rect.top=ship.rect.top

        # 存储用小数表示的子弹位置
        self.y=float(self.rect.y)

        self.color=ai_settings.bullet_color
        self.speed_factor=ai_settings.bullet_speed_factor



    def update(self, *args):
        '向上移动子弹'
        #更新表示子弹位置的小数值
        self.y-=self.speed_factor
        #更新表示子弹的rect的位置
        #向上变动
        # self.y-=1
        self.rect.y=self.y

    def draw_bullet(self):
        '在屏幕上绘制子弹'
        # self.screen.blit(self.screen,self.rect)
        pygame.draw.rect(self.screen,self.color,self.rect)
    def draw_bullet1(self):
        pass
        # self.screen.blit(self.image, self.rect)





