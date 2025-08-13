import random
import pygame
import asyncio

pygame.init()

screen_width = 1000
screen_height = 600

win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout Game")

black = (0, 0, 0)
white = (255, 255, 255)

colours = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
]

fps = 60
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)  

def write_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

async def gameloop():
    global win

    running = True
    game_over = False

    platform_width = 100
    platform_height = 20
    platform_speed = 8

    ball_size = 20
    ball_speed_x = 5
    ball_speed_y = -5

    box_width = 40
    box_height = 30

    platform = pygame.Rect((screen_width - platform_width) // 2,
                           screen_height - platform_height - 30,
                           platform_width, platform_height)
    ball = pygame.Rect(platform.centerx - ball_size // 2,
                       platform.top - ball_size,
                       ball_size, ball_size)

    boxes = []
    boxes_per_row = screen_width // box_width
    num_rows = 3  

    for row in range(num_rows):
        last_color = None
        for col in range(boxes_per_row):
            color = random.choice(colours)
            if col == 0:
                last_color = color
            if color == last_color:
                while color == last_color:
                    color = random.choice(colours)
            box = pygame.Rect(col * box_width, row * box_height, box_width, box_height)
            boxes.append((box, color))
            last_color = color

    while running:
        if game_over:
            win.fill(white)
            write_text("Game Over! Press Enter To Restart.", font, black,
                       win, screen_width // 2 - 330, screen_height // 2)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False  # Exit game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return True  # Restart game
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and platform.left > 0:
                platform.x -= platform_speed
            if keys[pygame.K_d] and platform.right < screen_width:
                platform.x += platform_speed

            ball.x += ball_speed_x
            ball.y += ball_speed_y

            if ball.left <= 0 or ball.right >= screen_width:
                ball_speed_x = -ball_speed_x
            if ball.top <= 0:
                ball_speed_y = -ball_speed_y

            if platform.colliderect(ball) and ball_speed_y > 0:
                ball_speed_y = -ball_speed_y
                ball_speed_x += random.choice([-1, 0, 1])

            if ball.top > screen_height:
                game_over = True

            for box in boxes:
                if box[0].colliderect(ball):
                    ball_speed_y = -ball_speed_y
                    ball_speed_x += random.choice([-1, 0, 1])
                    boxes.remove(box)
                    break

            if ball_speed_x > 6:
                ball_speed_x = 6
            if ball_speed_x < -6:
                ball_speed_x = -6

            win.fill(white)
            for box, color in boxes:
                pygame.draw.rect(win, color, box)
                pygame.draw.rect(win, black, box, 2)
            pygame.draw.rect(win, black, platform)
            pygame.draw.ellipse(win, (255, 0, 0), ball)

        pygame.display.update()
        await asyncio.sleep(0)
        clock.tick(fps)

async def main():
    while await gameloop():
        pass
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())