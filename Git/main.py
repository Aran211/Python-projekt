# Et saaks pygame käske kasutada impordime esialgu pygame.
# pygame saab installida pip install käsuga.
import pygame
import os
import random
from pygame import mixer

pygame.mixer.pre_init()
pygame.init()
font = pygame.font.Font("04B_19.ttf", 30)
score = 0
high_score = 0
# Siia faili tuleb peamine kood.
# ==============================

# Seame mängu akna laiuse ja kõrguse, caps lockis sellepärast,
# et need väärtused on konstantset. St. ei muutu.

WIDTH, HEIGHT = 600, 700
# Ütleme pygamele mis aken luua.
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# Pygame akna nimi.
pygame.display.set_caption("To Infinity")

# Konstantsed muutujad pildi suurustele.
RAKETT_WIDTH, RAKETT_HEIGHT = (40, 60)
METEOR_WIDTH, METEOR_HEIGHT = (30, 30)
FPS = 60

# Otsime samast kaustast kus .py fail kausta nimega Assets ja laeme
# sealt pildi oma programmi _IMAGE.
PLAYER_SPACESHIP = pygame.image.load(
    os.path.join('Assets', 'rakett1.png'))
# scalega vähendame piltide suurused korrektseks. rotatega pöörame.
# METEOR ja PLAYER_SPACESHIP on lõpuks need õiged objektid mis ekraanil
# liiguvad ja ilmuvad.
rakett = pygame.transform.rotate(pygame.transform.scale(
    PLAYER_SPACESHIP, (RAKETT_WIDTH, RAKETT_HEIGHT)), 270)
# Teha raketi ümber ristkülik, millega hiljem collisione tuvastada.
rakett_rect = rakett.get_rect(center=(40, 60))

# Teeme meteoriidiga sama. ilma rotateta sest seda pole vaja.
METEOR_IMAGE = pygame.image.load(os.path.join('Assets', 'meteoriit.png'))
METEOR = pygame.transform.scale(METEOR_IMAGE, (90, 80))

SPAWNMETEOR = pygame.USEREVENT
# EDIT : timer on väiksem.
pygame.time.set_timer(SPAWNMETEOR, 800)
# Suvalised meteoriitide kõrgused, millest random valitakse üks.
meteor_height = [50, 100, 200, 250, 300, 450, 550, 600]

TAUST_IMG = pygame.image.load(os.path.join(
    'Assets', 'Taust.jpg')).convert()  # Importin Tausta
TAUST = pygame.transform.scale(
    TAUST_IMG, (600, 700))  # Kohandan suuruse õigeks

jump_sound = pygame.mixer.Sound("Assets/Jump sound effect _ No copyright.mp3")
fail_sound = pygame.mixer.Sound(
    "Assets/Cartoon Falling Sound Effect(Copyright Free) (mp3cut.net).mp3")
# BG muusika.
background_music = mixer.music.load("Assets/Mercury.wav")
# -1 et mängiks loopi peal.
mixer.music.play(-1)


def create_meteor():
    random_meteor_pos = random.choice(meteor_height)
    meteor = METEOR.get_rect(midtop=(650, random_meteor_pos))
    return meteor


def move_meteors(meteors):
    for meteor in meteors:
        meteor.centerx -= 4
    return meteors


def draw_meteors(meteors):
    for meteor in meteors:
        WIN.blit(METEOR, meteor)


def check_collision(meteors):
    for meteor in meteors:
        if rakett_rect.colliderect(meteor):
            fail_sound.play()
            return False
        # Ekraanilt väljas kontroll.
        if rakett_rect.top <= -100 or rakett_rect.bottom >= 700:
            fail_sound.play()
            return False

    return True


def score_näitamine(game_state):
    global score
    # bug fixitud sellega et score uuendamine siin teha maini asemel.
    #score += 0.012

    if game_state == 'main_game':
        score_surface = font.render(
            'Time: '+str(int(score)), False, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        WIN.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = font.render(
            'Time: '+str(int(score)), False, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        WIN.blit(score_surface, score_rect)

        high_score_surface = font.render(
            'High Score: '+str(int(high_score)), False, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 300))
        WIN.blit(high_score_surface, high_score_rect)


def score_uuendamine():
    global score, high_score
    # kui skoor on suurem kui high score.
    if score > high_score:
        high_score = score
    return high_score


METEOR_LIST = []
score = 0
high_score = 0
# main loop.
# Siia paneme koodi mis jookseb lõputult nii kaua kui
# aken kinni pannakse või mängust lahkutakse.
# Mängu loogika kokkupõrked ja kõik selline tuleb siia.


def main():
    global score, high_score
    gravity = 0.25
    game_active = True
    raketi_liikumine = 0
    score = 0
    high_score = 0

    clock = pygame.time.Clock()
    run = True
    while run:
        # Selle mõte on see, et meie arvuti jookseks
        # koguaeg 60 kaadrit sekundis.
        clock.tick(FPS)
        # See kontrollib kogu aeg kas kasutaja pole veel lahkunud.
        # Kui on siis sulgeme mängu.
        # See kontrollib kas X on vajutatud.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:  # raketi kontrollimine
                if event.key == pygame.K_UP and game_active:
                    raketi_liikumine = 0
                    raketi_liikumine -= 7
                    jump_sound.play()
                if event.key == pygame.K_UP and game_active == False:
                    # Mäng kaotati ja alustatakse uuesti.
                    game_active = True
                    METEOR_LIST.clear()
                    rakett_rect.center = (100, 100)
                    raketi_liikumine = 0
                    score = 0

            if event.type == SPAWNMETEOR:
                METEOR_LIST.append(create_meteor())

        # Taust ja rakett luua.
        WIN.blit(TAUST, (0, 0))
        WIN.blit(rakett, (rakett_rect))

        if game_active:
            # Gravitatsioon raketile, et ta ei hõljuks.
            raketi_liikumine += gravity
            rakett_rect.centery += raketi_liikumine
            # Mäng tühistab töö kui rakett lendab vastu metoriiti
            game_active = check_collision(METEOR_LIST)

            # Meteoriidid
            meteor_list = move_meteors(METEOR_LIST)
            draw_meteors(meteor_list)
            check_collision(METEOR_LIST)

            # Skoor
            score += 0.012
            score_näitamine('main_game')
        else:
            # mäng on läbi.
            high_score = score_uuendamine()
            score_näitamine('game_over')

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
