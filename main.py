"""
mypygame
made using pycharm ide
built on pygame
Bill Erhard
bill.erhard@gmail.com
https://github.com/billerhard/mypygame/
"""
from PlayerProfile import PlayerProfile


def main():
    import sys
    import random
    import pygame

    pygame.init()
    size = width, height = 1280, 720
    black = 0, 0, 0
    screen = pygame.display.set_mode(size)
    ball = pygame.image.load("intro_ball.gif")
    ballrect = ball.get_rect()
    speed = [random.randint(1, 10), random.randint(1, 10)]
    pygame.font.init()
    bigsans = pygame.font.SysFont('Comic Sans MS', 30)
    clicku = False
    clickutimer = pygame.time.get_ticks()
    clickucolor = (255, 255, 255)
    player = PlayerProfile()
    scoresurface = bigsans.render('score = ' + str(player.score), False, (255, 255, 255))
    hitsurface = bigsans.render('hits = ' + str(player.hits) + ' crits = ' + str(player.crits), False, (255, 255, 255))
    smallsans = pygame.font.SysFont('Comic Sans MS', 16)

    clicklocation = pygame.mouse.get_pos()
    did_crit = False

    while 1:
        if clicku and pygame.time.get_ticks() - clickutimer > 1000:
            clicku = False
            did_crit = False
        pygame.time.delay(4)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicktop = pygame.mouse.get_pos()[1]
                clickleft = pygame.mouse.get_pos()[0]
                if ballrect.top < clicktop < ballrect.bottom and ballrect.left < clickleft < ballrect.right:
                    if not clicku:
                        clicku = True
                        player.hits += 1
                        player.score += 1
                        clicklocation = pygame.mouse.get_pos()
                        clickutimer = pygame.time.get_ticks()
                        if random.randint(0, 100) < player.crit_chance:
                            player.score += 1
                            player.crits += 1
                            did_crit = True

                        scoresurface = bigsans.render('score = ' + str(player.score), False, (255, 255, 255))
                        hitsurface = bigsans.render('hits = ' + str(player.hits) + ' crits = ' + str(player.crits),
                                                    False, (255, 255, 255))

        ballrect = ballrect.move(speed)
        if ballrect.left < 0:
            ballrect = ballrect.move(-speed[0], 0)
            speed[0] = random.randint(1, 4)
        elif ballrect.right > width:
            ballrect = ballrect.move(-speed[0], 0)
            speed[0] = -random.randint(1, 4)
        if ballrect.top < 0:
            ballrect = ballrect.move(0, -speed[1])
            speed[1] = random.randint(1, 4)
        elif ballrect.bottom > height:
            ballrect = ballrect.move(0, -speed[1])
            speed[1] = -random.randint(1, 4)
        screen.fill(black)
        screen.blit(ball, ballrect)
        if clicku:

            curtime = pygame.time.get_ticks()
            if (curtime - clickutimer) % 100 < 10:
                col1 = curtime % 3 * (255 / 3)
                col2 = (curtime + 1) % 3 * (255 / 3)
                col3 = (curtime + 2) % 3 * (255 / 3)
                clickucolor = (col1, col2, col3)
            if did_crit:
                clickusurface = bigsans.render('Critical Hit!', False, clickucolor)
                screen.blit(clickusurface, (0, 0))
                tempscore = "+2!!!"
            else:
                tempscore = "+1!"
            tempbox = smallsans.render(tempscore, False, (255, 255, 255))
            screen.blit(tempbox, clicklocation)
        screen.blit(scoresurface, (700, 0))
        screen.blit(hitsurface, (450, 0))
        pygame.display.flip()


if __name__ == "__main__":
    main()
