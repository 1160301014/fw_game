# *-* coding: utf-8 *-*
import random
import time
import pygame

PLANE_EMBEDDED_PIC = pygame.image.load('resources/image/shoot.png')
HERO_PIC_AREA_LIST = [(0, 99, 102, 126), (165, 360, 102, 126),
                      (165, 234, 102, 126), (330, 624, 102, 126),
                      (330, 498, 102, 126), (432, 624, 102, 126)]
ENEMY_PIC_AREA_LIST = [(534, 612, 57, 43), (267, 347, 57, 43),
                       (873, 697, 57, 43), (267, 296, 57, 43),
                       (930, 697, 57, 43)]
BULLET_PIC_AREA_LIST = [(1004, 987, 9, 21), ]
BACKGROUND_IMG_PATH = 'resources/image/background.png'
GAMEOVER_IMG_PATH = 'resources/image/gameover.png'
BULLET_SOUND_PATH = 'resources/sound/bullet.wav'
ENEMY_DOWN_SOUND_PATH = 'resources/sound/enemy1_down.wav'
GAMEOVER_SOUND_PATH = 'resources/sound/game_over.wav'
GAME_MAIN_MUSIC_PATH = 'resources/sound/game_music.wav'
SCREEN_SIZE = (480, 800)
WIDTH = 480
HEIGHT = 800
FRAME_RATE = 60


class Configer:
    """encapsulate several method of Providing data\n
    data includes sound,images\n
    field
    """

    def __init__(self, screen_size=(WIDTH, HEIGHT), frame_rate=FRAME_RATE, hero_ini_pos=[WIDTH / 2, HEIGHT],
                 ene_freq=1000, ene_speed=5, hero_speed=10, shoot_frequency=200):
        super().__init__()
        self.screen_size = screen_size
        self.width = self.screen_size[0]
        self.height = self.screen_size[1]
        self.frame_rate = frame_rate
        self.hero_ini_pos = hero_ini_pos
        self.enemy_period = ene_freq
        self.enemy_speed = ene_speed
        self.hero_speed = hero_speed
        self.shoot_period = shoot_frequency
        self.bg_img = self.get_bg_img()
        self.hero_img = self.get_hero_img()
        self.enemy_img = self.get_enemy_img()
        self.bullet_img = self.get_bullet_img()
        self.game_over_img = self.get_game_over_img()

    # unable to open file
    #  self.bullet_sound = self.get_bullet_sound()
    #  self.enemy_down_sound = self.get_enemy_down_sound()
    #  self.game_over_sound = self.get_game_over_sound()
    #  self.__play_game_main_music()

    @staticmethod
    def get_bg_img():
        return pygame.image.load(BACKGROUND_IMG_PATH)

    @staticmethod
    def get_hero_img():
        """return a list sorted by hero impaired degree"""
        hero_img = []
        for i in range(len(HERO_PIC_AREA_LIST)):
            hero_img.append(PLANE_EMBEDDED_PIC.subsurface(pygame.Rect(HERO_PIC_AREA_LIST[i])))
        return hero_img

    @staticmethod
    def get_enemy_img():
        enemy_img = []
        for i in range(len(ENEMY_PIC_AREA_LIST)):
            enemy_img.append(PLANE_EMBEDDED_PIC.subsurface(pygame.Rect(ENEMY_PIC_AREA_LIST[i])))
        return enemy_img

    @staticmethod
    def get_bullet_img():
        bullet_img = []
        for i in range(len(BULLET_PIC_AREA_LIST)):
            bullet_img.append(PLANE_EMBEDDED_PIC.subsurface(pygame.Rect(BULLET_PIC_AREA_LIST[i])))
        return bullet_img

    @staticmethod
    def get_game_over_img():
        return pygame.image.load(GAMEOVER_IMG_PATH)

    @staticmethod
    def get_bullet_sound(volume=0.3):
        bullet_sound = pygame.mixer.Sound(BULLET_SOUND_PATH)
        bullet_sound.set_volume(volume)
        return bullet_sound

    @staticmethod
    def get_enemy_down_sound(volume=0.3):
        enemy_down_sound = pygame.mixer.Sound(ENEMY_DOWN_SOUND_PATH)
        enemy_down_sound.set_volume(volume)
        return enemy_down_sound

    @staticmethod
    def get_game_over_sound(volume=0.3):
        game_over_sound = pygame.mixer.Sound(GAMEOVER_SOUND_PATH)
        game_over_sound.set_volume(volume)
        return game_over_sound

    def __play_game_main_music(self, music_play_para=(-1, 0.0), volume=0.25):
        pygame.mixer.music.load(GAME_MAIN_MUSIC_PATH)
        pygame.mixer.music.play(music_play_para)
        pygame.mixer.music.set_volume(volume)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, init_pos, bullet_img=Configer.get_bullet_img()[0], speed=10):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -self.rect.height:
            self.kill()


class Hero(pygame.sprite.Sprite):
    def __init__(self, init_pos, plane_img, bullets, speed=8):
        super().__init__()
        self.hero_img_list = plane_img
        self.hero_img_index = 0
        self.speed = speed
        self.bullets = bullets
        self.image = self.hero_img_list[self.hero_img_index]
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos

    def shoot(self):
        self.bullets.add(Bullet(self.rect.midtop))

    def move_up(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def move_down(self, screen_height):
        if self.rect.top >= screen_height - self.rect.height:
            self.rect.top = screen_height - self.rect.height
        else:
            self.rect.top += self.speed

    def move_right(self, screen_width):
        if self.rect.left >= screen_width - self.rect.width:
            self.rect.left = screen_width - self.rect.width
        else:
            self.rect.left += self.speed

    def move_left(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def got_damaged(self, step=1):
        """return true if enemy is dead,step must be 0 or 1"""
        if step != 0 and step != 1:
            raise Exception("step error:step==%s is illegal. Step must be 0 or 1" % str(step))
        self.hero_img_index += step
        if self.hero_img_index not in range(len(self.hero_img_list)):
            self.kill()
            return True
        self.image = self.hero_img_list[self.hero_img_index]
        return False


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, init_pos, speed=2):
        super().__init__()
        self.enemy_img_index = 0
        self.enemy_img_list = enemy_img
        self.speed = speed
        self.image = self.enemy_img_list[self.enemy_img_index]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = init_pos[0], init_pos[1]
        self.damaged = False

    def update(self, screen_height):
        if self.damaged:
            self.got_damaged()
            return
        self.rect.y += self.speed
        if self.rect.y > screen_height:
            self.kill()

    def got_damaged(self, step=1):
        """return true if enemy is dead,step must be 0 or 1"""
        if step != 0 and step != 1:
            raise Exception("step error:step==%s is illegal. Step must be 0 or 1" % str(step))
        self.enemy_img_index += step
        if self.enemy_img_index not in range(len(self.enemy_img_list)):
            self.kill()
            return True
        self.damaged = True
        self.image = self.enemy_img_list[self.enemy_img_index]
        return False

    def die(self):
        if self.got_damaged():
            self.kill()
        if self.got_damaged():
            self.kill()


class RollingBackground(pygame.sprite.Sprite):
    def __init__(self, bg_img, is_alt=False, speed=5):
        super().__init__()
        self.image = bg_img
        self.rect = bg_img.get_rect()
        self.speed = speed
        # self.rect.topleft((0, 0))
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        if self.rect.y < self.rect.height:
            self.rect.y += self.speed
        else:
            self.rect.y = -self.rect.height


class PlaneGame:
    """ main game class\n
    get data from DataSupplier

    """

    def __init__(self, config=Configer()):
        # define configer
        self.config = config
        # setup game screen
        pygame.init()
        self.screen = pygame.display.set_mode(self.config.screen_size)
        # setup game clock
        self.clock = pygame.time.Clock()
        # define event CREATE_ENEMY_EVENT
        self.CREATE_ENEMY_EVENT = pygame.USEREVENT
        self.SHOOT_EVENT = pygame.USEREVENT + 1
        # declare GAMEOVER not true
        self.GAMEOVER = False
        # self.
        # create sprites groups
        self.__create_sprites()
        # setup timer event
        pygame.time.set_timer(self.CREATE_ENEMY_EVENT, self.config.enemy_period)
        pygame.time.set_timer(self.SHOOT_EVENT, self.config.shoot_period)

    def start_game(self):
        while not self.GAMEOVER:
            # setup frame rate
            self.clock.tick(self.config.frame_rate)
            # check collision
            self.__check_collision()
            # update sprites
            self.__update_sprites()
            # update screen display
            pygame.display.update()
            # even handle
            self.__even_handler()
        pygame.quit()

    def __create_sprites(self):
        # create background
        self.bg_group = pygame.sprite.Group(RollingBackground(self.config.bg_img),
                                            RollingBackground(self.config.bg_img, True))
        # create enemies
        self.enemies_group = pygame.sprite.Group()
        # down enemies
        self.down_enemies_group = pygame.sprite.Group()
        # create bullets
        self.bullets_group = pygame.sprite.Group()
        # create hero
        self.hero = Hero(self.config.hero_ini_pos, self.config.hero_img, self.bullets_group, self.config.hero_speed)
        # create hero group
        self.hero_group = pygame.sprite.Group(self.hero)

    def __even_handler(self):
        for event in pygame.event.get():
            # click quit button to quit game
            if event.type == pygame.QUIT:
                self.__game_over()
            # add enemy to group when CREATE_ENEMY_EVENT occurs
            if event.type == self.CREATE_ENEMY_EVENT:
                ene_x = random.randint(0, self.config.width)
                self.enemies_group.add(Enemy(self.config.enemy_img,
                                             [ene_x, 0],
                                             self.config.enemy_speed)
                                       )
            if event.type == self.SHOOT_EVENT:
                self.hero.shoot()
        # click K_Right/K_Left/K_Up/K_Down to move hero
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.move_right(self.config.width)
        if keys_pressed[pygame.K_LEFT]:
            self.hero.move_left()
        if keys_pressed[pygame.K_UP]:
            self.hero.move_up()
        if keys_pressed[pygame.K_DOWN]:
            self.hero.move_down(self.config.height)

    def __check_collision(self):
        # when collide,send damage message to inform hero and enemies of playing destroyed animation
        sg_collide_list = pygame.sprite.spritecollide(self.hero, self.enemies_group, True)
        if len(sg_collide_list) and self.hero.got_damaged():
            self.__game_over()
        down_enemies = pygame.sprite.groupcollide(self.enemies_group, self.bullets_group, False, True).keys()
        self.down_enemies_group.add(down_enemies)
        for d_ene in down_enemies:
            d_ene.die()

    def __update_sprites(self):
        self.bg_group.update()
        self.bg_group.draw(self.screen)
        self.enemies_group.update(self.config.height)
        self.enemies_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        self.bullets_group.update()
        self.bullets_group.draw(self.screen)
        self.down_enemies_group.update(self.config.height)
        self.down_enemies_group.draw(self.screen)

    def __game_over(self):
        self.GAMEOVER = True


if __name__ == "__main__":
    launcher = PlaneGame()
    launcher.start_game()
