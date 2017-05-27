from classes import *


def main(width, height):
    # Death counter
    deaths = 0
    clock = pygame.time.Clock()
    pygame.init()
    font = pygame.font.SysFont("OSP-DIN", 48)

    # create the screen
    dimensions = (width, height)
    screen = pygame.display.set_mode(dimensions)

    # helps with making the close button in the corner work
    running = 1

    # The ground
    level = Level(screen, width, height, "resources/Level 1.png")

    # The character, who's sprite is a gingerbread man
    gingerman = Character(screen, width, height)

    coin_imgs = ["resources/Coin2.png", "resources/Coin.png"]
    # The clouds. We put them into a list so we can iterate through them
    clouds = [Cloud(), Cloud(), Cloud()]
    coins = []
    powerups = []
    rocks = [
        ItemOnGround(screen, width, height, 'resources/stone.png', random.randint(-2 * width, 2 * width), height - 150,
                     True)
        for _ in range(10)]
    bullets = []
    for x in range(7):
        coins.append(
            ItemOnGround(screen, width, height, random.choice(coin_imgs),
                         (random.randint(-4000, 4000)) - (10 * x) + width,
                         height - 150))
        powerups.append(
            PowerUp(screen, width, height, 'resources/arrow.png', (random.randint(-4000, 4000)) - (10 * x) + width,
                    height - 150))

    # If the arrow keys are held down, we want the character to continously move. This helps with that.
    pygame.key.set_repeat(100, gingerman.speed)

    might_be_bullet = None

    # Gameloop, executes all the actions
    while running:

        # Gets a list of what's happening
        events = pygame.event.get()

        # Reads the list of what's happening
        for event in events:

            # Exits program if red X cliked
            if event.type == pygame.QUIT:
                running = 0
                # sys.exit()

            # Moves the character if the keys are pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    gingerman.move(level, 'left', coins, powerups)
                if event.key == pygame.K_RIGHT:
                    gingerman.move(level, 'right', coins, powerups)
                if event.key == pygame.K_SPACE:
                    gingerman.move(level, 'up', coins, powerups)
                if event.key == pygame.K_q:
                    print("shoot(self, velocity)")
                    might_be_bullet = gingerman.shoot(level, -1)
                if event.key == pygame.K_w:
                    might_be_bullet = gingerman.shoot(level, 1)
            if might_be_bullet is not None:
                bullets.append(might_be_bullet)
                might_be_bullet = None

        # makes the background blue
        screen.fill((135, 206, 235))

        # Shows the level
        level.display()

        for coin in coins:
            coin.display(gingerman, level)
        for thing in powerups:
            thing.display(gingerman, level)

        deathtext = font.render("Score:" + str(gingerman.deaths), 1, (255, 255, 255))
        rocktext = font.render("Rocks:" + str(gingerman.rocks), 1, (255, 255, 255))

        for rock in rocks:
            rock.display(gingerman, level)

        for bullet in bullets:
            bullet.fly()

        # Makes sure physics applies
        gingerman.move(level, 'forward', coins)
        # print(gingerman)
        # Shows and moves the cloud
        for cloud in clouds:
            cloud.move()

        screen.blit(deathtext, (0, 0))
        screen.blit(rocktext, (0, 48))

        # Shows everything
        pygame.display.flip()

        clock.tick(60)


if __name__ == '__main__':
    main(1024, 576)
