import pygame
import random
import sys

pygame.init()

clock = pygame.time.Clock()
fps = 70

screen_width = 996
screen_height = 563

# загружаем картинки
desertbg = pygame.image.load('images/desert.png')
junglebg = pygame.image.load('images/junglebg1.png')
junglegr = pygame.image.load('images/junglegr.png')
skybg = pygame.image.load('images/sky.jpg')
skygr = pygame.image.load('images/ccc.png')
startbg = pygame.image.load('images/startbg.png')
ground_img = pygame.image.load('images/desertgr.png')
rstrtbutton_img = pygame.image.load('images/rstbtn.png')
startbtn = pygame.image.load('images/strtbtn.png')
menubtn = pygame.image.load('images/menubtn.png')
fon2 = pygame.image.load('images/fon2.png')
fon2_jun = pygame.image.load('images/junglessmini.png')
fon2_des = pygame.image.load('images/desmini.png')
fon2_sky = pygame.image.load('images/skymini.png')

# определяем шрифт и цвет
font = pygame.font.SysFont('Realest', 60)
font2 = pygame.font.SysFont('Realest', 40)
black = (0, 0, 0)

# переменные
ground_move = 0
move_speed = 4
flying = False
game_over = False
stolb_rast = 170
stolb_speed = 1500
last_stolb = pygame.time.get_ticks()
score = 0
plus_stolb = False
skyfon = False
junfon = False
desfon = False
number_page = 1


# стартовая страничка
def start_screen():
    fon = pygame.transform.scale(startbg, (screen_width, screen_height))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif strtbtn.draw():
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


# вторая страничка выбора фона
def second_page():
    global skyfon, junfon, desfon
    fon = pygame.transform.scale(fon2, (screen_width, screen_height))
    screen.blit(fon, (0, 0))

    while True:
        with open('score.txt', 'r') as f:
            try:
                mx = max([line for line in f])
            except:
                mx = 0
        f.close()

        textt(f'Ваш рекорд: {mx[:-1]}', font2, black, 750, screen_height - 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif junglebtn.draw() or dessertbtn.draw() or skybtn.draw():
                if skybtn.draw():
                    skyfon = True
                    junfon = False
                    desfon = False
                if junglebtn.draw():
                    junfon = True
                    desfon = False
                    skyfon = False
                if dessertbtn.draw():
                    desfon = True
                    skyfon = False
                    junfon = False
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Birdd')


def textt(text, font, colour, x, y):
    img = font.render(text, True, colour)
    screen.blit(img, (x, y))


def rstrt_game():
    stolb_group.empty()
    bird.rect.x = 100
    bird.rect.y = int(screen_height / 2)
    score = 0
    return score


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for i in range(1, 3):
            img = pygame.image.load(f"images/b{i}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.velocity = 0
        # чтобы не летел вверх долго при нажатии
        self.clicked = False

    def update(self):

        if flying:
            # падение птицы
            self.velocity += 0.5
            if self.velocity > 8:
                self.velocity = 8
            if self.rect.bottom < 485:
                self.rect.y += int(self.velocity)

        if not game_over:
            # прыжок птицы
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.velocity = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # анимация птички
            flaps = 6
            self.counter += 1

            if self.counter > flaps:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # наклон птицы для красоты
            self.image = pygame.transform.rotate(self.images[self.index], (self.velocity * -2))
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Stolb(pygame.sprite.Sprite):
    def __init__(self, x, y, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/pipee.png')
        self.rect = self.image.get_rect()
        # pos 1 сверху pos -1 снизу
        if pos == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(stolb_rast / 2)]
        if pos == -1:
            self.rect.topleft = [x, y + int(stolb_rast / 2)]
        # pos 1 сверху pos -1 снизу

    def update(self):
        self.rect.x += ground_move
        if self.rect.right < 0:
            self.kill()


class Btn():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        act = False
        # позиция мыши
        pos = pygame.mouse.get_pos()
        # проверяем находится ли мышка на кнопке
        if self.rect.collidepoint(*pos):
            if pygame.mouse.get_pressed()[0] == 1:
                act = True

        screen.blit(self.image, (self.rect.x - 55, self.rect.y + 43))
        return act


stolb_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()
bird = Bird(100, int(screen_height / 2))
bird_group.add(bird)

rstrtbtn = Btn(300, screen_height // 2 - 92, rstrtbutton_img)
strtbtn = Btn(screen_width // 2 - 10, screen_height // 2 - 80, startbtn)
junglebtn = Btn(90, 2, fon2_jun)
dessertbtn = Btn(400, 2, fon2_des)
skybtn = Btn(710, 2, fon2_sky)
menubtn = Btn(600, screen_height // 2 - 100, menubtn)

run = True
while run:
    clock.tick(fps)
    if number_page == 1:
        start_screen()
        number_page = 2
    elif number_page == 2:
        second_page()
        number_page = 3
    else:
        if skyfon:
            screen.blit(skybg, (0, 0))
        if junfon:
            screen.blit(junglebg, (0, 0))
        if desfon:
            screen.blit(desertbg, (0, 0))

        bird_group.draw(screen)
        bird_group.update()
        stolb_group.draw(screen)

        # добавление земли
        if desfon:
            screen.blit(ground_img, (0, 485))
        if junfon:
            screen.blit(junglegr, (0, 480))
        if skyfon:
            screen.blit(skygr, (0, 420))

        # проверка счета
        if len(stolb_group) > 0:
            if bird_group.sprites()[0].rect.left > stolb_group.sprites()[0].rect.left \
                    and bird_group.sprites()[0].rect.right < stolb_group.sprites()[0].rect.right \
                    and not plus_stolb:
                plus_stolb = True
            if plus_stolb:
                if bird_group.sprites()[0].rect.left > stolb_group.sprites()[0].rect.right:
                    score += 1
                    plus_stolb = False

        textt(str(score), font, black, int(screen_width / 2), 20)

        # столкновение
        if pygame.sprite.groupcollide(bird_group, stolb_group, False, False) or bird.rect.top < 0:
            game_over = True

        # проверка на то, что птица ударилась о землю
        if bird.rect.bottom > 485:
            game_over = True
            flying = False

        if not game_over and flying:
            # создание новых столбов
            time_now = pygame.time.get_ticks()
            if time_now - last_stolb > stolb_speed:
                stolb_height = random.randint(-100, 100)
                btm_stolb = Stolb(screen_width, int(screen_height / 2) + stolb_height, -1)
                top_stolb = Stolb(screen_width, int(screen_height / 2) + stolb_height, 1)
                stolb_group.add(btm_stolb)
                stolb_group.add(top_stolb)
                last_stolb = time_now

            # движение земли
            ground_move -= move_speed
            if abs(ground_move) > 9:
                ground_move = 0

            stolb_group.update()

        # проверяем то, что игра закончилась и начинаем заново
        if game_over:
            if menubtn.draw():
                game_over = False
                with open('score.txt', 'a') as f:
                    f.write(str(score))
                    f.write("\n")
                    f.close()
                score = rstrt_game()
                number_page = 2
                # second_page()
            if rstrtbtn.draw():
                game_over = False
                with open('score.txt', 'a') as f:
                    f.write(str(score))
                    f.write("\n")
                    f.close()
                score = rstrt_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
                flying = True

        pygame.display.update()

pygame.quit()
