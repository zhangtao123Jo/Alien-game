import sys
import pygame
from bullet import Bullet
from alien import Alien
from bullet1 import Bullet1
import random
biaozi=1
from time import sleep



def check_keydown_events(event,ai_settings,screen,ship,bullets,bullets1):
    '响应按钮'
    if event.key == pygame.K_RIGHT:
        # 向右移动飞船
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        #向左
        ship.moving_left = True
    if event.key==pygame.K_UP:
        #向上
        ship.moving_up=True
    if event.key==pygame.K_DOWN:
        #向下
        ship.moving_down=True

    if event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets,bullets1)

    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event,ship):
    '响应松开'
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key==pygame.K_UP:
        #向上
        ship.moving_up=False
    if event.key==pygame.K_DOWN:
        #向下
        ship.moving_down=False



def fire_bullet(ai_settings,screen,ship,bullets,bullets1):
    if len(bullets) < ai_settings.bullets_allowed:
        # 创建一个子弹，并将其加入当编组BULLETS中
        new_bullet = Bullet(ai_settings, screen, ship)
        new_bullet1 = Bullet1(ai_settings, screen, ship)
        bullets.add(new_bullet)
        bullets1.add(new_bullet1)
    # if len(bullets1) < ai_settings.bullets_allowed:
        # 创建一个子弹，并将其加入当编组BULLETS中
        # bullets1.add(new_bullet)

def check_events(ai_settings, screen,stats,sb,play_button, ship, aliens,bullets,bullets1):
    '响应按键和鼠标事件'
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            #飞船移动响应事件
            check_keydown_events(event,ai_settings, screen, ship, bullets,bullets1)
        elif event.type==pygame.KEYUP:
            check_keyup_events(event,ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats,sb, play_button, ship, aliens,bullets,bullets1, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats,sb, play_button, ship, aliens,bullets,bullets1, mouse_x, mouse_y):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        sb.setleft(3)
        ai_settings.initialize_dynamic_settings()
        #隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        bullets1.empty()

        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens,bullets,bullets1, play_button):
    # while True:
        img2 = pygame.image.load(r'images\70.jpg').convert_alpha()
        '更新屏幕上的图像，并切换当心屏幕'

        # screen.fill(ai_settings.bg_color)
        screen.blit(img2,(0,0))
        # 在飞船和外星人后面重绘所有子弹
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        for bullet1 in bullets1.sprites():
            bullet1.draw_bullet1()
        #每次更新屏幕需要从新绘制飞船的当前位置
        ship.blitme()
        # alien.blitme()
        aliens.draw(screen)

        # Scoreboard.show_score(sb)
        # 显示得分
        sb.prep_score()
        sb.show_score()
        #更新等级
        sb.prep_level()

        # 如果游戏处于非活动状态，就显示Play按钮
        if not stats.game_active:
            play_button.draw_button()
        # 让最近绘制的屏幕可见
        pygame.display.flip()


def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets,bullets1):
    #更新子弹的位置
    bullets.update()
    #删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    bullets1.update()
    for bullet1 in bullets1.copy():
        if bullet1.rect.bottom <= 0:
            bullets1.remove(bullet1)

    #检查是否有子弹击中了外星人
    #如果是这样，就删除相映的子弹和外星人
    collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
        # stats.score += ai_settings.alien_points
            sb.prep_ships()
            sb.prep_score()
        #检查是否诞生了新的最高得分
        check_high_score(stats,sb)
    # collisions1=pygame.sprite.groupcollide(bullets1, aliens, True, True)
    if len(aliens)==0 :
        global biaozi
        biaozi+=1

        #将等级提升
        stats.level += 1
        print(stats.level)
        #将外星飞船移动速度左右提升
        ai_settings.alien_speed_factor+=2
        #将外星飞船上下移动提升
        if biaozi%10==0:
            ai_settings.fleet_drop_speed+=10
        print(ai_settings.fleet_drop_speed,'上下')
        print(ai_settings.alien_speed_factor)

        #删除现有的子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings,screen,ship,aliens)
    # check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets,bullets1)


def create_fleet(ai_settings,screen,ship,aliens):
    #创建一个外星人，计算按一行可容纳多少个外星人
    #外星人间距为外星人宽度
    alien=Alien(ai_settings,screen)
    number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
    # number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.hight)

    #创建第一行外星人
    for row_number in range(biaozi):
        # alien.rect.y =
        for alien_number in range(number_aliens_x):
            #创建一个外星人并将其键入当前行
            x=random.choice(['1','0','2'])
            if x=='1':
                 create_alien(ai_settings,screen,aliens,alien_number,row_number)


def get_number_aliens_x(ai_settings,alien_width):
    #计算每行可容纳多少个外星人
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2* alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number,row_number):
    #创建外星人群
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y=alien.rect.y+2*alien.rect.y*row_number
    aliens.add(alien)

def get_number_rows(ai_settings,ship_height,alien_height):
    '计算屏幕可容纳多少行外星人'
    available_space_y = (ai_settings.screen_height- (3*alien_height)-ship_height)
    number_rows=int(available_space_y/(2*alien_height))
    return number_rows

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets,bullets1):
    """检查是否有外星人位于屏幕边缘,更新外星人群中所有外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets,bullets1)
        print('Ship hit!!!')
    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets,bullets1)


def change_fleet_direction(ai_settings, aliens):
        '将整群外星人下移，并改变他们的方向'
        for alien in aliens.sprites():
            alien.rect.y+=ai_settings.fleet_drop_speed
            # if alien.rect.y>=10:
            #     biaozi=True
            # else:
            #     biaozi=False
        ai_settings.fleet_direction*=-1


def check_fleet_edges(ai_settings,aliens):
    '有外星人到达边缘时采用响应的措施'
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets,bullets1):
    """响应被外星人撞到的飞船"""
    # 将ships_left减1
    if stats.ship_left > 0:
        # 减去性命
        stats.ship_left -= 1

        sb.setleft(stats.ship_left)
        # 更新记分牌
        sb.prep_ships()
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # 暂停
        sleep(1)
    else:
        stats.game_active=False
        pygame.mouse.set_visible(True)
        if stats.ship_left==0 and stats.score>stats.high_score:
            stats.high_score=stats.score


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,bullets,bullets1):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets,bullets1)
            break

# def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,aliens, bullets,bullets1):
#     """响应子弹和外星人发生碰撞"""
#     # 删除发生碰撞的子弹和外星人
#     collisions = pygame.sprite.groupcollide(bullets, bullets1,aliens, True, True)
#     if len(aliens) == 0:
#         # 删除现有的子弹，加快游戏节奏，并创建一群新的外星人
#         bullets.empty()
#         bullets1.empty()
#         ai_settings.increase_speed()
#
#         # 提高等级
#         stats.level += 1
#         sb.prep_level()
#
#         create_fleet(ai_settings, screen, ship, aliens)
#
#
#     if collisions:
#         for aliens in collisions.values():
#             stats.score += ai_settings.alien_points * len(aliens)
#             sb.prep_score()
#         check_high_score(stats, sb)
#     #
#     pass

def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
