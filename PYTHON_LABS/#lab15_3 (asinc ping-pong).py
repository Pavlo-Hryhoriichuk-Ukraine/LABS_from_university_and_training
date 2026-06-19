
#lab15_3 (asinc ping-pong)
import pygame
import asyncio

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
COLOR_BG = (30,30,30)

BALL_RADIUS = 20
BALL_COLOR_RGB = (255,100,100)

FPS = 144

RACKET_WIDTH_1 = 15
RACKET_HEIGHT_1 = 60
RACKET_COLOR_1 = (90,85,30)

RACKET_WIDTH_2 = 15
RACKET_HEIGHT_2 = 60
RACKET_COLOR_2 = (135,50,70)



async def main():

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    
    ball_x = WINDOW_WIDTH // 2
    ball_y = WINDOW_HEIGHT // 2
    ball_rect = pygame.Rect(ball_x,ball_y,20,20)
    ball_speed_x = 2.2
    ball_speed_y = 1.2
    
    racket_1_x = 0
    racket_1_y = WINDOW_HEIGHT // 2 + 60
    racket_1_speed = 3
    racket_left_1 = pygame.Rect(racket_1_x, racket_1_y, 30, 60)

    racket_2_x = WINDOW_WIDTH - 30
    racket_2_y = WINDOW_HEIGHT // 2 + 60
    racket_2_speed = 3
    racket_left_2 = pygame.Rect(racket_2_x, racket_2_y, 30, 60)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #якщо хрестик на вікні натиснули
                running = False
        
        keys = pygame.key.get_pressed() #бо якщо event то це тільки одне натискання, а тут можна затискати клавіші 
        if keys[pygame.K_w]:
            racket_left_1.y -= racket_1_speed
        if keys[pygame.K_s]:
            racket_left_1.y += racket_1_speed
        if keys[pygame.K_UP]:
            racket_left_2.y -= racket_2_speed
        if keys[pygame.K_DOWN]:
            racket_left_2.y += racket_2_speed

        ball_rect.x += ball_speed_x
        ball_rect.y -= ball_speed_y

        if ball_rect.x - BALL_RADIUS < 0 or ball_rect.x + BALL_RADIUS > WINDOW_WIDTH:
            running = False

        if ball_rect.colliderect(racket_left_1) or ball_rect.colliderect(racket_left_2):
            ball_speed_x = -ball_speed_x

        if ball_rect.y - BALL_RADIUS < 0 or ball_rect.y + BALL_RADIUS > WINDOW_HEIGHT:
            ball_speed_y = -ball_speed_y
            
        if racket_left_1.bottom >= WINDOW_HEIGHT:
            racket_left_1.bottom = WINDOW_HEIGHT
        
        if racket_left_1.top <= 0:
            racket_left_1.top = 0

        if racket_left_2.bottom >= WINDOW_HEIGHT:
            racket_left_2.bottom = WINDOW_HEIGHT
        
        if racket_left_2.top <= 0:
            racket_left_2.top = 0
        
        screen.fill(COLOR_BG)

        pygame.draw.circle(screen, BALL_COLOR_RGB, ball_rect[:-2], BALL_RADIUS)
        pygame.draw.rect(screen, RACKET_COLOR_1, racket_left_1)
        pygame.draw.rect(screen,RACKET_COLOR_2, racket_left_2)
        pygame.display.flip()
        await asyncio.sleep(1/FPS)
    
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())