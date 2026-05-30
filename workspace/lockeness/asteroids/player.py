import pygame
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.shotgun_timer = 0

    # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        self.timer -= dt
        self.shotgun_timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)
        
        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_s]:
            self.move(-dt)

        if keys[pygame.K_SPACE]:
            self.shoot()

    def move(self, dt):
        start_vector = pygame.Vector2(0,1)
        rotated_vector = start_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        if self.timer > 0:
            return

        self.timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        direction = pygame.Vector2(0, 1).rotate(self.rotation)

        if self.shotgun_timer > 0:
            for angle in [-15, 0, 15]:
                spread_direction = direction.rotate(angle)
                new_shot = Shot(self.position.x, self.position.y)
                new_shot.velocity = spread_direction * PLAYER_SHOOT_SPEED
                
        else:
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = direction * PLAYER_SHOOT_SPEED

    def activate_shotgun(self):
        self.shotgun_timer = 10
