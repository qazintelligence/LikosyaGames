import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((612,382))
pygame.display.set_caption("қызық ойын типа")
icon = pygame.image.load('images/6936483_game_gaming_play_icon.png').convert_alpha()
pygame.display.set_icon(icon)


bg = pygame.image.load('images/background.jpeg').convert_alpha()
walk_left = [
    pygame.image.load('images/left/player1.png').convert_alpha(),
    pygame.image.load('images/left/player2.png').convert_alpha(),
    pygame.image.load('images/left/player3.png').convert_alpha(),
    pygame.image.load('images/left/player4.png').convert_alpha()
]
walk_right = [
    pygame.image.load('images/right/player5.png').convert_alpha(),
    pygame.image.load('images/right/player6.png').convert_alpha(),
    pygame.image.load('images/right/player7.png').convert_alpha(),
    pygame.image.load('images/right/player8.png').convert_alpha()
]

player_anim_count = 0
bg_x = 0

monster = pygame.image.load('images/bakeneko.png').convert_alpha()
monster_list_in_game = []

DEFAULT_IMAGE_SIZE = (40,40)

image = pygame.transform.scale(monster, DEFAULT_IMAGE_SIZE)

player_speed = 7
player_x = 150
player_y = 265

is_jump = False
jump_count = 8

bg_sound = pygame.mixer.Sound('sounds/Нуртас - Байка.mp3')
bg_sound.play()

monster_timer = pygame.USEREVENT + 1
pygame.time.set_timer(monster_timer,2500)

label = pygame.font.Font('fonts/OpenSans_Condensed-Bold.ttf',40)
lose_label = label.render('Siz ūtyldynyz!', True, 'White')
restart_label = label.render('Qaita oinau', True, (193, 214, 152))
restart_label_rect = restart_label.get_rect(topleft=(230,200))

bullets_left = 5
bullett = pygame.image.load('images/bullet.png').convert_alpha()
bullet  = pygame.transform.scale(bullett, (20,20))
bullets = []

gameplay = True

running = True
while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 612, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x,player_y))

        if monster_list_in_game:
            for (i,el) in enumerate(monster_list_in_game):
                screen.blit(image, el)
                el.x -= 10

                if el.x < -10:
                    monster_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 250:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_UP]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2)/2
                else:
                    player_y += (jump_count ** 2)/2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8


        if player_anim_count == 3:
           player_anim_count = 0
        else:
            player_anim_count+=1

        bg_x -= 3
        if bg_x == -612:
            bg_x = 0


        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet,(el.x,el.y))
                el.x += 5

                if el.x > 620:
                    bullets.pop(i)
                if monster_list_in_game:
                    for (index, image_el) in enumerate(monster_list_in_game):
                        if el.colliderect(image_el):
                            monster_list_in_game.pop(index)
                            bullets.pop(i)
    else:
        screen.fill((63, 64, 61))
        screen.blit(lose_label,(220,127))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            monster_list_in_game.clear()
            bullets.clear()
            bullets_left = 5

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == monster_timer:
            monster_list_in_game.append(image.get_rect(topleft=(615,275)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_RSHIFT and bullets_left>0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 30)))
            bullets_left -= 1

    clock.tick(20)