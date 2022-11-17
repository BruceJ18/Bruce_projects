import pygame
import os
pygame.font.init()

# Window
WIDTH, HEIGHT = 1200, 900
WIND = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jungle Survival")
jungle_image = pygame.transform.scale(pygame.image.load(os.path.join('pixel_images', 'pixel_jungle.png')),(WIDTH, HEIGHT))
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
LOZER_FONT = pygame.font.SysFont("comicsans", 200)
FPS = 60

# colors
RED = (200, 5, 5)
WHITE = (255, 255, 255)
GREEN = (50, 100, 10)

# dimensions
indie_width, indie_height = 55, 70
spider_width, spider_height = 80, 70

# indie
indie_image = pygame.image.load(os.path.join('pixel_images', 'pixel_indie.png'))
indie_rdir = pygame.transform.scale(indie_image, (indie_width, indie_height))
indie_ldir = pygame.transform.flip(indie_rdir, True, False)
indie_hit = pygame.USEREVENT
indie_count = 0
indie_health = 5
indie_dy = 0
floor_limit_indie = 900 - indie_height


# spider
spider_image = pygame.image.load(os.path.join("pixel_images", "pixel_spider.png"))
spider_ldir = pygame.transform.rotate(pygame.transform.scale(spider_image, (spider_width, spider_height)), -10)
spider_rdir = pygame.transform.flip(spider_ldir, True, False)
floor_limit_spider = 900 - spider_height
crawl_count = 0
spider_vel = 12
spider_left = False
spider_right = False


gravity = 4


def indie_movement_y(indie):
    global indie_dy
    if indie_dy > 0 or indie.y < floor_limit_indie:
        indie.y -= indie_dy
        indie_dy -= gravity
    if indie.y > floor_limit_indie:
        indie.y = floor_limit_indie
    if indie.y == floor_limit_indie and indie_dy < 0:
        indie_dy = 0


def collision(indie, spider):
    global indie_health
    if indie.colliderect(spider):
        pygame.event.post(pygame.event.Event(indie_hit))
        indie.x -= 10
        indie.x += 20
        indie.y -= 20


def show_on_wind(indie, spider):
    WIND.blit(jungle_image, (0, 0))
    indie_health_text = HEALTH_FONT.render("Health: " + str(indie_health), True, WHITE)
    WIND.blit(indie_health_text, (0, 0))
    WIND.blit(indie_rdir, (indie.x, indie.y))
    WIND.blit(spider_ldir, (spider.x, spider.y))

    pygame.display.update()


def indie_movement_x(indie):
    indie_vel_x = 5
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_RIGHT] and indie.x <= WIDTH - indie_width:
        indie.x += indie_vel_x
    if keys_pressed[pygame.K_LEFT] and indie.x >= 0:
        indie.x -= indie_vel_x


def lose(text):
    draw_text = LOZER_FONT.render(text, True, RED)
    WIND.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(2000)


def main():
    global indie_health
    global floor_limit_indie
    global indie_dy

    indie = pygame.Rect(100, floor_limit_indie, indie_width, indie_height)
    spider = pygame.Rect(WIDTH - spider_width, floor_limit_spider, spider_width, spider_height)


    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        show_on_wind(indie, spider)
        indie_movement_x(indie)
        # spider_movement(spider)
        collision(indie, spider)
        indie_movement_y(indie)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == indie_hit:
                indie_health -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and indie_dy == 0:
                    indie_dy = 50
        lose_text = ""
        if indie_health <= 0:
            lose_text = "You lose"
        if lose_text != "":
            lose(lose_text)
            break





    pygame.quit()


if __name__ == "__main__":
    main()
