import pygame
class Settings():
    '存储《外星人入侵》的所有设置的类'
    def __init__(self):
        '初始化游戏的设置'
        #屏幕设置
        self.screen_width=1500
        self.screen_height=900
        self.bg_color=(255,228,181)
        # self.img2 = pygame.image.load(r'D:\学习资料\py\论文毕设\images\70.jpg')
        #飞船的设置
        self.ship_speed_factor=20.5
        #子弹设置
        #子弹速度
        self.bullet_speed_factor=50
        #宽高
        self.bullet_width=5
        self.bullet_height=15
        self.bullet_color=(237,138,75)
        self.ship_limit=3
        #弹夹数目
        self.bullets_allowed=100
        # 外星人设置
        self.alien_speed_factor=0
        self.fleet_drop_speed = 10
        # fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = -1
        #加快游戏节奏
        self.speedup_scale=1.1
        # 外星人点数的提高速度
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        #飞船速度
        self.ship_speed_factor = 40
        #子弹速度
        self.bullet_speed_factor = 50
        #外星人速度
        self.alien_speed_factor = 30
        # fleet_direction为1表示向右；为-1表示向左
        self.fleet_direction = 1

        #记分
        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
