import pygame, sys,random

pygame.init()
clock = pygame.time.Clock()
screenWidth = 500
screenHeight = 640
screen = pygame.display.set_mode((screenWidth,screenHeight))
icon = pygame.image.load("Flappy_Bird_icon.png")
background = pygame.image.load("sprites/background_day.png")
background = pygame.transform.scale(background, (500,800))



get_ready = pygame.transform.scale_by(pygame.image.load("sprites/getready.png"), 0.8)
tap = pygame.image.load("sprites/tap.png")


gameover_board = pygame.image.load("sprites/board.png")
gameover_caption = pygame.image.load("sprites/gameover.png")
point = pygame.mixer.Sound("audio/point.wav")

die = pygame.mixer.Sound("audio/die.wav")
die_play = 0

frequency = 0
pygame.display.set_icon(icon)
pygame.display.set_caption("FlappyBird")

flap = pygame.mixer.Sound("audio/wing.wav")
direction = 0
gravity = 0.9 

passpipe = False
class Bird(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()
        self.sprite = []
        self.sprite.append(pygame.image.load("sprites/midflapbird.png"))
        self.sprite.append(pygame.image.load("sprites/downflapbird.png"))
        self.sprite.append(pygame.image.load("sprites/upflapbird.png"))
        self.current_sprite = 0
        self.image = self.sprite[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.gravity = 0
        self.direction = 0
    def rotate(self):
        rotated_bird = pygame.transform.rotozoom(self.image,-self.direction*3,1)
        self.image = rotated_bird

    def update(self):

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.gravity = 0.5
        
        if self.rect.bottom < screenHeight:
            self.rect.y += self.direction
            self.direction+= self.gravity
        self.current_sprite+=0.15

        if self.current_sprite >= len(self.sprite):
            self.current_sprite =0
        self.image = self.sprite[int(self.current_sprite)]
        
    def go_up(self):
        self.direction = -8
bird = Bird(screenWidth//2-100,screenHeight//2)
bird_group = pygame.sprite.Group()
bird_group.add(bird)
pipe_gap = random.randrange(130, 180)

moving = False

class Pipes(pygame.sprite.Sprite):
    def __init__(self,x,y,pos):
        super().__init__()
        self.image = pygame.image.load("sprites/pipe.png")
        self.rect = self.image.get_rect()

        if pos == 1:
            self.image = pygame.transform.flip(self.image, False, True)

            self.rect.bottomleft = [x,y]
        if pos == -1:
            self.rect.topleft = [x,y + pipe_gap]
    def update(self):
        if moving ==True:

            self.rect.x -= 3.5 


pipetop = Pipes(screenWidth,int(screenHeight/3),1)
pipebottom = Pipes(screenWidth, int(screenHeight/3), -1)
pipe_group = pygame.sprite.Group()
pipe_group.add(pipetop)
pipe_group.add(pipebottom)

base = pygame.image.load("sprites/base.png")
base1 = pygame.image.load("sprites/base.png")
base_pos = 0
base1_pos = 500
play_die = False
gameover= False
speed = 0
recent_pipe_x = 0
score = 0
multi_digit_score = []


scores = []

scores.append(pygame.image.load("sprites/0.png"))
scores.append(pygame.image.load("sprites/1.png"))
scores.append(pygame.image.load("sprites/2.png"))
scores.append(pygame.image.load("sprites/3.png"))
scores.append(pygame.image.load("sprites/4.png"))
scores.append(pygame.image.load("sprites/5.png"))
scores.append(pygame.image.load("sprites/6.png"))
scores.append(pygame.image.load("sprites/7.png"))
scores.append(pygame.image.load("sprites/8.png"))
scores.append(pygame.image.load("sprites/9.png"))


alpha = 255
multidigit = False
pipe_gap_time = 1500
while True:
    frequency +=speed
    for event in pygame.event.get():
        if event.type  == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if gameover == False:
                    flap.play()
                    bird.go_up()
                    moving = True
                    speed = 14
  



    pygame.display.flip()
    screen.blit(background,(0,-100))
    if moving == True and gameover == False:
        pipe_group.draw(screen)
        pipe_group.update()

    screen.blit(base, (base_pos,550))
    screen.blit(base1, (base1_pos,550))


    if gameover == False:
        if score<=9:
            screen.blit(scores[score], (screenWidth//2-15, 45))
        if score >9:
            screen.blit(scores[score//10], (screenWidth/2-30, 45))
            screen.blit(scores[score%10], (screenWidth/2, 45))
        if moving  ==True:
            alpha -=5
            tap.set_alpha(alpha)
            get_ready.set_alpha(alpha)
        screen.blit(tap, (220, 280))
        screen.blit(get_ready, (90, 130))


 




    if gameover == False and moving==True: 
        base_pos-=3.5
        base1_pos-=3.5

        if base_pos<= -500:
            base_pos = 500
        if base1_pos <=-500:
            base1_pos = 500

        if frequency >= pipe_gap_time:

            height_variety = random.randrange(-150,100)

            pipetop = Pipes(screenWidth,int(screenHeight/3) + height_variety,1)
            pipebottom = Pipes(screenWidth, int(screenHeight/3)+ height_variety, -1)

            pipe_group.add(pipetop)
            pipe_group.add(pipebottom)
            frequency = 0
        if pipe_group.sprites()[0].rect.right < 0:
            pipe_group.remove(pipe_group.sprites()[0])
        pipe_gap_time -= 0.001




    bird_group.draw(screen)
    if gameover == False:
        bird_group.update()
        bird.rotate()


    clock.tick(60)

        

    if pygame.sprite.groupcollide(bird_group,pipe_group, False,False ) or bird_group.sprites()[0].rect.top <= 0 or bird_group.sprites()[0].rect.bottom >= 540:
        if die_play == 0:
            die.play()
            die_play+=1
        gameover = True
        moving = False
    if gameover == True:

        screen.blit(gameover_board, (screenWidth/2-170, 200))
        screen.blit(gameover_caption, (70, 100))
        if score<=9:
            screen.blit(pygame.transform.scale_by(scores[score], 0.8), (380, 250))
        if score >9:
            screen.blit(pygame.transform.scale_by(scores[score//10], 0.8), (365, 250))
            screen.blit(pygame.transform.scale_by(scores[score%10], 0.8), (390, 250))

        if bird.rect.y <= 505:
            bird.rect.y += direction
            direction += gravity
    if gameover == False:
        if len(pipe_group) > 0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and passpipe == False:
                passpipe = True
            if passpipe == True and bird_group.sprites()[0].rect.left > pipe_group.sprites()[1].rect.right:
                point.play()
                score +=1
    
                passpipe = False
                print(score)











