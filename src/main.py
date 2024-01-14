import time
import pygame
from sys import exit
from random import randint

from config import *
from sprites import *


class Game:
    ACTIVE_STATE = 1
    INACTIVE_STATE = 0
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(CAPTION)
        self.displaySurface = pygame.display.set_mode(WINDOW_WH)
        self.fpsClock = pygame.time.Clock()
        icon = pygame.image.load("resources/Player/bird1.png").convert_alpha()
        pygame.display.set_icon(icon)

        self.allSprites = pygame.sprite.Group()
        self.collisionSprites = pygame.sprite.Group()
        self.coinSprites = pygame.sprite.Group()

        Background(self.allSprites)
        Ground([self.allSprites, self.collisionSprites], self.allSprites.sprites()[0].yScaleFactor)
        self.player = Player(self.allSprites, self.allSprites.sprites()[0].yScaleFactor)
        
        self.obstacleTimer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacleTimer, 1400)
        
        self.font = pygame.font.Font(FONT_SRC, FONT_SIZE)
        self.score = -1
        self.coin = -1
        self.gameState = Game.INACTIVE_STATE
        self.config_audio()

        
    def config_audio(self):
        self.jumpSE = pygame.mixer.Sound("resources/Audio/wing.wav")
        self.coinSE = pygame.mixer.Sound("resources/Audio/point.wav")
        self.hitSE = pygame.mixer.Sound("resources/Audio/hit.wav")
        self.dieSE = pygame.mixer.Sound("resources/Audio/die.wav")
        self.jumpSE.set_volume(SE_VOLUME)
        self.coinSE.set_volume(SE_VOLUME)
        self.hitSE.set_volume(SE_VOLUME)
        self.dieSE.set_volume(SE_VOLUME)

    def check_collisions(self):
        if pygame.sprite.spritecollide(self.player, self.collisionSprites, False)\
            or self.player.rect.top <= 0:
            self.hitSE.play()
            self.gameState = Game.INACTIVE_STATE
            self.dieSE.play()
            
        if pygame.sprite.spritecollide(self.player, self.coinSprites, True):
            self.coinSE.play()
            self.coin += 1
            
    def reset(self):
        [obj.kill() for obj in self.collisionSprites.sprites()[1:]]
        [obj.kill() for obj in self.coinSprites]
        self.player.reset_sprite()
        self.score = 0
        self.coin = 0
        self.gameState = Game.ACTIVE_STATE

    def display_stat(self):
        if self.gameState == Game.ACTIVE_STATE: self.score += 0.15
        
        if self.gameState == Game.INACTIVE_STATE:
            if self.score == -1 or self.coin == -1:
                y1 = y2 = -1000
            else:
                y1 = (WINDOW_WH[1] / 2) - 40
                y2 = y1 + 30
            y3 = (WINDOW_WH[1] / 2) - 100
            y4 = y3 - 50
        else:
            y1 = WINDOW_WH[1] / 21
            y2 = WINDOW_WH[1] / 10
            y3 = -10000
            y4 = y3
            
        msgBgImg = pygame.image.load("resources/Background/box.png")
        msgBgImg = pygame.transform.scale(msgBgImg, pygame.math.Vector2(msgBgImg.get_size()) / 4)
        msgBgImgRect = msgBgImg.get_rect(topleft = (0, y4))
            
        startMsgSurface = self.font.render("HIT SPACE TO START", False, "Black")
        startMsgRect = startMsgSurface.get_rect(midtop = ((WINDOW_WH[0] + 17) / 2, y3))
        
        scoreSurface = self.font.render(f"Score : {int(self.score)}", False, "Black")
        scoreRect = scoreSurface.get_rect(midtop = ((WINDOW_WH[0] + 17) / 2, y1))
        
        coinSurface = self.font.render(f"Coin : {self.coin}", False, "Black")
        coinRect = coinSurface.get_rect(midtop = ((WINDOW_WH[0] + 17) / 2, y2))
        
        self.displaySurface.blit(msgBgImg, msgBgImgRect)
        self.displaySurface.blit(startMsgSurface, startMsgRect)
        self.displaySurface.blit(scoreSurface, scoreRect)
        self.displaySurface.blit(coinSurface, coinRect)

    def run(self):
        lastTime = time.time()
        while True:
            deltaTime = time.time() - lastTime
            lastTime = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.gameState == Game.ACTIVE_STATE:
                            self.jumpSE.play()
                            self.player.jump()
                        else:
                            self.reset()

                elif event.type == self.obstacleTimer:
                    for itr in range(0, randint(1, 2)):
                        Pipe([self.allSprites, self.collisionSprites], self.allSprites.sprites()[0].yScaleFactor)
                    
                    for itr in range(0, randint(1, 3)):
                        Coin([self.allSprites, self.coinSprites], self.allSprites.sprites()[0].yScaleFactor, self.collisionSprites.sprites())

            self.allSprites.draw(self.displaySurface)
            
            if self.gameState == Game.ACTIVE_STATE:
                self.allSprites.update(deltaTime)
                self.check_collisions()
                
            self.display_stat()
            
            pygame.display.update()
            
            self.fpsClock.tick(MAX_FPS)


if __name__ == "__main__":
    Game().run()