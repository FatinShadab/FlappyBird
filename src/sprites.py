import pygame
from config import *
from random import choice, randint


class Background(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        srcImage = pygame.image.load("resources/Background/sky_bg.png").convert_alpha()
        self.srcImgHeight = srcImage.get_height()
        self.srcImgWidth = srcImage.get_width()
        self.yScaleFactor = WINDOW_WH[1] / self.srcImgHeight

        fullSizedImage = pygame.transform.scale(srcImage, (self.srcImgWidth * self.yScaleFactor, self.srcImgHeight * self.yScaleFactor))
        
        self.image = pygame.Surface((self.srcImgWidth * self.yScaleFactor * 2, self.srcImgHeight * self.yScaleFactor))
        self.image.blit(fullSizedImage, (0, 0))
        self.image.blit(fullSizedImage, ((self.srcImgWidth - 1) * self.yScaleFactor, 0))

        self.rect = self.image.get_rect(topleft = (0, 0))
        self.posVector = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.posVector.x -= 150 * dt
        
        if self.rect.centerx <= 0:
            self.posVector.x = 0

        self.rect.x = round(self.posVector.x)


class Ground(pygame.sprite.Sprite):
    def __init__(self, groups, scaleFactor):
        super().__init__(groups)
        
        groundSurf = pygame.image.load("resources/Background/ground_bg.png").convert_alpha()
        fullSizedImage = pygame.transform.scale(groundSurf, pygame.math.Vector2(groundSurf.get_size()) * scaleFactor)

        self.image = pygame.Surface((int(groundSurf.get_width() * scaleFactor * 2), int(groundSurf.get_height() * scaleFactor)))
        self.image.blit(fullSizedImage, (0, 0))
        self.image.blit(fullSizedImage, (groundSurf.get_width() * scaleFactor, 0))
        
        self.rect = self.image.get_rect(bottomleft = (0, WINDOW_WH[1] + 50))
        self.posVector = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.posVector.x -= 200 * dt
        
        if self.rect.centerx <= 0:
            self.posVector.x = 0

        self.rect.x = round(self.posVector.x)


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, scaleFactor):
        super().__init__(groups)

        self.import_image(scaleFactor)
        self.frameIndex = 0
        self.image = self.frames[self.frameIndex]

        self.rect = self.image.get_rect(midleft = ((WINDOW_WH[0] - 400) / 2,(WINDOW_WH[1] - 10) / 2)).inflate(-50, -10)
        self.posVector = pygame.math.Vector2(self.rect.topleft)

        self.gravity = 700
        self.acc = 0

    def import_image(self, scaleFactor):
        self.frames = []
        print(scaleFactor)

        for itr in range(1, 5):
            surf = pygame.image.load(f"resources/Player/bird{itr}.png").convert_alpha()
            scaledSurface = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scaleFactor * 5)

            self.frames.append(scaledSurface)

    def apply_gravity(self, dt):
        self.acc += self.gravity * dt
        self.posVector.y += self.acc * dt
        self.rect.y = round(self.posVector.y)

    def jump(self):
        self.acc = -313

    def animate(self, dt):
        self.frameIndex += 7 * dt
        if self.frameIndex >= len(self.frames):
            self.frameIndex = 0

        self.image = self.frames[int(self.frameIndex)]
        
    def reset_sprite(self):
        self.frameIndex = 0
        self.image = self.frames[self.frameIndex]

        self.rect = self.image.get_rect(midleft = ((WINDOW_WH[0] - 400) / 2,(WINDOW_WH[1] - 10) / 2))
        self.posVector = pygame.math.Vector2(self.rect.topleft)
        
        self.gravity = 700
        self.acc = 0

    def rotate(self, dt):
        rotatedPlayer = pygame.transform.rotozoom(self.image, -1 * self.acc * dt * 2, 1)
        self.image = rotatedPlayer

    def update(self, dt):
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate(dt)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, groups, scaleFactor):
        super().__init__(groups)

        orientation = choice(("up", "down"))
        surf = pygame.image.load(f"resources/Tiles/pipe{choice(range(1, 4))}.png")
        self.image = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scaleFactor * 5.5)
        
        x = WINDOW_WH[0] + randint(60, 120)
        
        if orientation == "up":
            y = WINDOW_WH[1] + 10
            self.rect = self.image.get_rect(midbottom = (x, y))
        else:
            y = -10
            self.rect = self.image.get_rect(midtop = (x, y))
            
        self.posVector = pygame.math.Vector2(self.rect.topleft)
        
    def update(self, dt):
        self.posVector.x -= 400 * dt
        self.rect.x = round(self.posVector.x)
        
        if self.rect.right <= -100:
            self.kill()
            

class Coin(pygame.sprite.Sprite):
    def __init__(self, groups, scaleFactor, sprites):
        super().__init__(groups)
        
        self.import_image(scaleFactor)
        self.frameIndex = 0
        self.image = self.frames[self.frameIndex]
        
        generated = False
        while not generated:
            x = WINDOW_WH[0] + choice(list(range(40, 80)))
            y = choice(list(range(200, 650)))

            self.rect = self.image.get_rect(center=(x, y))
            overlapping = any(pipe.rect.colliderect(self.rect) for pipe in sprites)
            
            if not overlapping:
                generated = True
    
        self.posVector = pygame.math.Vector2(self.rect.topleft)
        
    def import_image(self, scaleFactor):
        self.frames = []
        
        for itr in range(0, 6):
            surf = pygame.image.load(f"resources/Coins/coin{itr}.png").convert_alpha()
            scaledSurface = pygame.transform.scale(surf, (pygame.math.Vector2(surf.get_size()) * scaleFactor) / 5)
            
            self.frames.append(scaledSurface)
        
    def animate(self, dt):
        self.frameIndex += 7 * dt
        
        if self.frameIndex >= len(self.frames):
            self.frameIndex = 0
        
        self.image = self.frames[int(self.frameIndex)]

    def update(self, dt):
        self.animate(dt)
        self.posVector.x -= 400 * dt
        self.rect.x = round(self.posVector.x)
        
        if self.rect.right <= -100:
            self.kill()