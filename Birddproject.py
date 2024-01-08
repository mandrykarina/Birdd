import pygame
import random


pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 563

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Birdd')

# загружаем картинки
mainbg = pygame.image.load('images/desert.png')
startbg = pygame.image.load('images/startbg.png')
ground_img = pygame.image.load('images/desertgr.png')
rstrtbutton_img = pygame.image.load('images/rstbtn.png')

# определяем шрифт и цвет
font = pygame.font.SysFont('Realest', 60)
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


class Rstrtbtn():
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

rstrtbtn = Rstrtbtn(screen_width // 2 - 50, screen_height // 2 - 100, rstrtbutton_img)

run = True
while run:

    clock.tick(fps)

    # добавление заднего фона
    screen.blit(mainbg, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    stolb_group.draw(screen)

    # добавление земли
    screen.blit(ground_img, (0, 485))

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
        if rstrtbtn.draw():
            game_over = False
            score = rstrt_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True

    pygame.display.update()

pygame.quit()
