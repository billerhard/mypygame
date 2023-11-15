"""
mypygame
made using pycharm ide
just kidding now it's vs code
built on pygame
Bill Erhard
bill.erhard@gmail.com
https://github.com/billerhard/mypygame/
"""

import sys
from random import randint
from pygame import font, image, time, display, mouse, event, MOUSEBUTTONDOWN, QUIT
from pygame import init as pygameinit

from player_profile import PlayerProfile


def init_pygame():
    """pygame inits"""
    pygameinit()
    font.init()


def init_screen():
    """init and return screen"""
    size = 1280, 720
    return size[0], size[1], display.set_mode(size)


def init_colors():
    """init and return colors"""
    return 0, 0, 0


def rainbowize_color(curtime):
    """returns a random color based on time"""
    col1 = curtime % 3 * (255 / 3)
    col2 = (curtime + 1) % 3 * (255 / 3)
    col3 = (curtime + 2) % 3 * (255 / 3)
    return (col1, col2, col3)


def check_crit(player):
    """given player, check crit, return true if crit"""
    if randint(0, 100) < player.player_data[3]:
        player.score += 1
        player.crits += 1
        return True
    return False


def update_score(f, player):
    """resets score surface"""
    return f.render(f"score = {player.player_data[0]}", False, (255, 255, 255))


def update_hits(f, player):
    """resets hit surface"""
    return f.render(
        f"hits = {player.player_data[1]} crits = {player.player_data[2]}",
        False,
        (255, 255, 255),
    )


def update_clicku(f, curtime):
    """resets clicku surface"""
    return f.render("Critical Hit!", False, rainbowize_color(curtime))


def check_hit(ballrect):
    """checks that mousepos is within ball bounds returns bool"""
    clickleft, clicktop = mouse.get_pos()
    if (
        ballrect.top < clicktop < ballrect.bottom
        and ballrect.left < clickleft < ballrect.right
    ):
        return True
    return False


def handle_events(sd, so):
    """handles user input events"""
    for e in event.get():
        if e.type == QUIT:
            sys.exit()
        if e.type == MOUSEBUTTONDOWN and not sd["clicku"] and check_hit(so["ballrect"]):
            sd["clicku"] = True
            sd["player"].hits += 1
            sd["player"].score += 1
            sd["clicklocation"] = mouse.get_pos()
            sd["clickutimer"] = time.get_ticks()
            sd["did_crit"] = check_crit(sd["player"])
            so["scoresurface"] = update_score(so["bigsans"], sd["player"])
            so["hitsurface"] = update_hits(so["bigsans"], sd["player"])


def main():
    """main function"""

    width, height, screen = init_screen()
    init_pygame()
    colors = init_colors()

    speed = [randint(1, 10), randint(1, 10)]
    try:
        player = PlayerProfile.load(1)
    except AttributeError:
        print("could not find player with id 1.")
        print(f"player: {PlayerProfile.load(1)}")
        player = PlayerProfile()
    sessiondata = {
        "clicku": False,
        "clickutimer": time.get_ticks(),
        "player": player,
        "clicklocation": mouse.get_pos(),
        "did_crit": False,
    }
    screenobjects = {
        "ball": image.load("intro_ball.gif"),
        "bigsans": font.SysFont("Comic Sans MS", 30),
        "smallsans": font.SysFont("Comic Sans MS", 16),
    }
    screenobjects["ballrect"] = screenobjects["ball"].get_rect()
    screenobjects["scoresurface"] = update_score(
        screenobjects["bigsans"], sessiondata["player"]
    )
    screenobjects["hitsurface"] = update_hits(
        screenobjects["bigsans"], sessiondata["player"]
    )

    while 1:
        if (
            sessiondata["clicku"]
            and time.get_ticks() - sessiondata["clickutimer"] > 1000
        ):
            sessiondata["clicku"] = False
        time.delay(8)
        handle_events(sessiondata, screenobjects)

        screenobjects["ballrect"] = screenobjects["ballrect"].move(speed)
        if screenobjects["ballrect"].left < 0:
            screenobjects["ballrect"] = screenobjects["ballrect"].move(-speed[0], 0)
            speed[0] = randint(1, 4)
        elif screenobjects["ballrect"].right > width:
            screenobjects["ballrect"] = screenobjects["ballrect"].move(-speed[0], 0)
            speed[0] = -randint(1, 4)
        if screenobjects["ballrect"].top < 0:
            screenobjects["ballrect"] = screenobjects["ballrect"].move(0, -speed[1])
            speed[1] = randint(1, 4)
        elif screenobjects["ballrect"].bottom > height:
            screenobjects["ballrect"] = screenobjects["ballrect"].move(0, -speed[1])
            speed[1] = -randint(1, 4)
        screen.fill(colors)
        screen.blit(screenobjects["ball"], screenobjects["ballrect"])
        if sessiondata["clicku"]:
            tempscore = "+1!"
            curtime = time.get_ticks()
            if sessiondata["did_crit"]:
                clickusurface = update_clicku(screenobjects["bigsans"], curtime)
                screen.blit(clickusurface, (0, 0))
                tempscore = "+2!!!"
            tempbox = screenobjects["smallsans"].render(
                tempscore, False, (255, 255, 255)
            )
            screen.blit(tempbox, sessiondata["clicklocation"])
        screen.blit(screenobjects["scoresurface"], (700, 0))
        screen.blit(screenobjects["hitsurface"], (450, 0))
        display.flip()
        sessiondata["player"].save()


if __name__ == "__main__":
    main()
