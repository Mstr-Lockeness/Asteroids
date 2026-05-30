from constants import SCREEN_HEIGHT, SCREEN_WIDTH, POWERUP_RADIUS
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from powerup import Powerup
import random
import sys
import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group() 
    powerups = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)
    Powerup.containers = (updatable, drawable, powerups)
    asteroid_field = AsteroidField()
    font = pygame.font.Font(None, 36)
    score = 0
    dt = 0
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updatable.update(dt)
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    drop_pos = asteroid.position
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
                    score += 1
                    if random.random() < .05:
                        new_powerup = Powerup(drop_pos.x, drop_pos.y, POWERUP_RADIUS)
                        new_shotgun_velocity = pygame.Vector2(0, 1).rotate(random.uniform(0, 360))
                        new_powerup.velocity = new_shotgun_velocity * 100 
        for p_up in powerups:
            if p_up.collides_with(player):
                log_event("powerup_collected")
                player.activate_shotgun()
                p_up.kill()
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print(f"Game over! Your score is {score}")
                sys.exit()
        for item in drawable:
            item.draw(screen)
        score_surf = font.render(f"Score: {score}", True, "white")
        screen.blit(score_surf, (10, 10))
        pygame.display.flip()
        dt = clock.tick(60) / 1000

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")


if __name__ == "__main__":
    main()