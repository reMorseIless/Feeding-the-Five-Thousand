import pygame
from pygame import math as pygame_math
import random
import os
import sys
import classes

def addPath(r_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(os.path.dirname(__file__), f"assets/{r_path}")

Clock = pygame.time.Clock()
timer = 0
State = "SplashscreenOpen"
Framerate = 60

#Images
splashscreen = pygame.image.load(addPath("splashscreen2.0.png"))
titlescreenbg = pygame.image.load(addPath("titlescreenbg.png"))
gamebg = pygame.image.load(addPath("gamebg.png"))
secretImage = pygame.image.load(addPath("funnything.png"))
tutorialPage = pygame.image.load(addPath("tutorial.png"))
storyBackgrounds = [
    pygame.image.load(addPath("storypics/story0.png")),
    pygame.image.load(addPath("storypics/story1.png")),
    pygame.image.load(addPath("storypics/story2.png")),
    pygame.image.load(addPath("storypics/story3.png")),
    pygame.image.load(addPath("storypics/story4.png")),
    pygame.image.load(addPath("storypics/story5.png"))
]
animatedtitleList = sorted(os.listdir(addPath("titlescreen")))
animatedplaybtList = sorted(os.listdir(addPath("playbuttonframes")))
animatedstorybtList = sorted(os.listdir(addPath("storybuttonframes")))
animatedsecretbtList = sorted(os.listdir(addPath("secretbuttonframes"))) #very efficient

startY = 420
foodCooldown = 0
score = 0
lives = 5
foods = []
people = []
isBread = True

storyTexts = [
    [
        "After hearing about John the Baptist's death, Jesus went to",
        "a deserted space to pray quietly. Many people followed Jesus,",
        "including his twelve disciples."
    ],
    [
        "Jesus saw that many of them were sick and healed them.",
        "However, when evening came, his disciples urged him to send",
        "the five thousand people away so they could eat."
    ],
    [
        "Despite their requests, Jesus insisted that they could eat from",
        "the food they prepared. But the disciples said they only brought",
        "five loaves of bread and two fish."
    ],
    [
        "Hearing this, Jesus asked the disciples for the food, and",
        "ordered the crowds to sit on the grass."
    ],
    [
        "Taking the bread and fish, he looked to heaven, blessed the food,",
        "and broke the bread. His disciples then passed the loaves of",
        "bread and fish among the crowds to eat."
    ],
    [
        "Despite the initially meager portions, everyone was able to eat",
        "until they were full. The crowds then gathered the leftovers,",
        "and filled twelve baskets full!"
    ]
]

pygame.init()

#Fonts
storyFont = pygame.font.Font(addPath("storytext.ttf"),25)
scoreFont = pygame.font.Font(addPath("storytext.ttf"),18)
finalscreenFont = pygame.font.Font(addPath("storytext.ttf"),40)
finalscreenlostFont = pygame.font.Font(addPath("storytext.ttf"),65)

Window = pygame.display.set_mode((800, 600))
tempSurface = pygame.Surface(Window.get_size(), pygame.SRCALPHA)
pygame.display.set_caption("Feeding the Five Thousand")
pygame.display.set_icon(pygame.image.load(addPath("icon.png")))

playRect = pygame.Rect(0, 0, 113, 37)
playRect.center = (400, 300)
storyRect = pygame.Rect(0, 0, 113, 37)
storyRect.center = (400, 350)
secretRect = pygame.Rect(0, 0, 113, 37)
secretRect.center = (400, 400)
mScreenbts = [playRect, storyRect, secretRect]

def set_state(state: str):
    global State, timer
    State = state
    timer = 0

def dialogue_len(dList : list):
    length = 0
    for text in dList:
        length += len(text)
    return length

def animate_fade(into : bool, bgimage : pygame.Surface):
    global timer
    timer += 1
    Window.fill((0, 0, 0))
    Window.blit(bgimage, (0, 0))
    if into:
        pygame.draw.rect(tempSurface, (0, 0, 0, pygame_math.clamp(255 - 255 * (timer / 20), 0, 255)),(0, 0, Window.get_width(), Window.get_height()))
    else:
        pygame.draw.rect(tempSurface, (0, 0, 0, pygame_math.clamp(255 * (timer / 20), 0, 255)),(0, 0, Window.get_width(), Window.get_height()))
    Window.blit(tempSurface, (0, 0))
    Clock.tick(20)

def loadImage(imagePath: str, centerX: int, centerY: int):
    image = pygame.image.load(addPath(imagePath))
    imageRect = image.get_rect()
    imageRect.center = (centerX, centerY)
    Window.blit(image, imageRect)

def fade_m_screen(into : bool):
    global timer
    timer += 1
    Window.blit(titlescreenbg, (0, 0))
    loadImage("titlescreen/frame_72_delay-0.51s.png", 400, 150)
    loadImage("playbuttonframes/frame_26_delay-1.14s.png", 400, 300)
    loadImage("storybuttonframes/frame_26_delay-1.14s.png", 400, 350)
    loadImage("secretbuttonframes/frame_26_delay-1.14s.png", 400, 400)
    if into:
        pygame.draw.rect(tempSurface, (0, 0, 0, pygame_math.clamp(255 - 255 * (timer / 20), 0, 255)),(0, 0, Window.get_width(), Window.get_height()))
    else:
        pygame.draw.rect(tempSurface, (0, 0, 0, pygame_math.clamp(255 * (timer / 20), 0, 255)),(0, 0, Window.get_width(), Window.get_height()))
    Window.blit(tempSurface, (0, 0))
    Clock.tick(20)

def fade_game(into : bool):
    global timer
    timer += 1
    Window.blit(gamebg, (0, 0))
    #start button here later
    if into:
        tRect = tutorialPage.get_rect()
        tRect.center = (400, 300)
        Window.blit(tutorialPage, tRect)
        pygame.draw.rect(tempSurface, (0, 0, 0, pygame_math.clamp(255 - 255 * (timer / 20), 0, 255)),(0, 0, Window.get_width(), Window.get_height()))
    else:
        pygame.draw.rect(tempSurface, (0, 0, 0, pygame_math.clamp(255 * (timer / 20), 0, 255)),(0, 0, Window.get_width(), Window.get_height()))
    Window.blit(tempSurface, (0, 0))
    Clock.tick(20)

def render_jesus():
    chosenSprite : pygame.Surface = None
    if isBread:
        chosenSprite = pygame.image.load(addPath("JesusSprites/Bread.png"))
    else:
        chosenSprite = pygame.image.load(addPath("JesusSprites/Fish.png"))
    rect = chosenSprite.get_rect()
    rect.center = (pygame_math.clamp(pygame.mouse.get_pos()[0], 50, 750), 100)
    Window.blit(chosenSprite, rect)

def rollForPerson():
    if timer < 7200 and random.randint(1, 100) == 1:
        return True
    elif 7200 <= timer < 14400 and random.randint(1, 60) == 1:
        return True
    elif 14400 <= timer < 20000 and random.randint(1, 30) == 1:
        return True
    elif 20000 <= timer < 35000 and random.randint(1, 10) == 1:
        return True
    elif 35000 <= timer and random.randint(1, 7) == 1:
        return True
    return False

while State != "Quit":
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            State = "Quit"
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if State == "WaitForResponse":
                for i, rect in enumerate(mScreenbts):
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        State = f"mScreenFadeOutTo{i}"
                        break
            elif State == "gameplaying":
                if foodCooldown > 15:
                    foodCooldown = 0
                    if isBread:
                        newBread = classes.Food("bread", pygame.mouse.get_pos()[0])
                        foods.append(newBread)
                    else:
                        newFish = classes.Food("fish", pygame.mouse.get_pos()[0])
                        foods.append(newFish)
            elif State == "tutorialScreen":
                if 343 <= pygame.mouse.get_pos()[0] <= 459 and 429 <= pygame.mouse.get_pos()[1] <= 467:
                    set_state("gameplaying")
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_e and State == "gameplaying":
            isBread = not isBread

    if State == "SplashscreenOpen":
        if timer < 20:
            animate_fade(True, splashscreen)
        else:
            set_state("SplashscreenWait")
    elif State == "SplashscreenWait":
        if timer < 120:
            timer += 1
        else:
            set_state("SplashscreenClose")
    elif State == "SplashscreenClose":
        if timer < 30:
            animate_fade(False, splashscreen)
        else:
            set_state("WaitForTitle")
    elif State == "WaitForTitle":
        if timer < 120:
            timer += 1
        else:
            set_state("OpenTitle")
    elif State == "OpenTitle":
        if timer < 30:
            animate_fade(True, titlescreenbg)
        else:
            set_state("AnimateTitle")
    elif State == "loadMain":
        if timer < 30:
            fade_m_screen(True)
        else:
            set_state("WaitForResponse")
    elif State == "AnimateTitle":
        if timer < len(animatedtitleList):
            Window.blit(titlescreenbg, (0, 0))
            currName = animatedtitleList[timer]
            delay = int(round((1/(float(currName[-9:-5])))*1.35, 0))
            loadedFrame = pygame.image.load(os.path.join(addPath("titlescreen"), currName))
            loadedFrameRect = loadedFrame.get_rect()
            loadedFrameRect.center = (400, 150)
            Window.blit(loadedFrame, loadedFrameRect)
            timer += 1
            Framerate = delay
        else:
            Framerate = 60
            set_state("AppearTSPlay")
    elif State == "AppearTSPlay":
        Framerate = int(round(1/0.03))
        if timer < len(animatedplaybtList)+14:
            Window.blit(titlescreenbg, (0, 0))
            loadImage("titlescreen/frame_72_delay-0.51s.png", 400, 150)
            if timer < len(animatedplaybtList):
                currName = animatedplaybtList[timer]
                loadedFrame = pygame.image.load(os.path.join(addPath("playbuttonframes"), currName))
                loadedFrameRect = loadedFrame.get_rect()
                loadedFrameRect.center = (400, 300)
                Window.blit(loadedFrame, loadedFrameRect)
            else:
                loadImage("playbuttonframes/frame_26_delay-1.14s.png", 400, 300)
            if timer >= 7 and timer < len(animatedplaybtList)+7:
                currName = animatedstorybtList[timer-7]
                loadedFrame = pygame.image.load(os.path.join(addPath("storybuttonframes"), currName))
                loadedFrameRect = loadedFrame.get_rect()
                loadedFrameRect.center = (400, 350)
                Window.blit(loadedFrame, loadedFrameRect)
            elif timer >= 7:
                loadImage("storybuttonframes/frame_26_delay-1.14s.png", 400, 350)
            if timer >= 14 and timer < len(animatedplaybtList) + 14:
                currName = animatedsecretbtList[timer - 14]
                loadedFrame = pygame.image.load(os.path.join(addPath("secretbuttonframes"), currName))
                loadedFrameRect = loadedFrame.get_rect()
                loadedFrameRect.center = (400, 400)
                Window.blit(loadedFrame, loadedFrameRect)
            timer += 1
        else:
            Framerate = 60
            set_state("WaitForResponse")
    elif State.find("mScreenFadeOutTo") != -1:
        if timer < 30:
            fade_m_screen(False)
        else:
            set_state(f"loadScreen{State[-1:]}")
    elif State.find("loadScreen") != -1:
        if State[-1:] == "2":
            animate_fade(True, secretImage)
        elif State[-1:] == "1":
            if timer < 30:
                animate_fade(True, storyBackgrounds[0])
            else:
                set_state("story0")
        elif State[-1:] == "0":
            if timer < 30:
                fade_game(True)
            else:
                lives = 5
                score = 0
                foodCooldown = 0
                isBread = True
                set_state("tutorialScreen")
    elif State == "fadeOutStory":
        if timer < 30:
            animate_fade(False, storyBackgrounds[5])
        else:
            set_state("loadMain")
    elif State[0:5] == "story":
        currentIndexstr = State[-1:]
        timerMax = dialogue_len(storyTexts[int(currentIndexstr)])
        Framerate = 30
        if timer < timerMax:
            Window.blit(storyBackgrounds[int(currentIndexstr)], (0, 0))
            totalCharsReached = 0
            reachedi = -1
            for i, text in enumerate(storyTexts[int(currentIndexstr)]):
                if reachedi != i:
                    totalCharsReached += len(text)
                    reachedi = i
                if totalCharsReached < timer:
                    render = storyFont.render(text, True, (30, 30, 30))
                    Window.blit(render, (10, startY+(33*i)))
                else:
                    render = storyFont.render(text[0:len(text)-(totalCharsReached-timer)+1], True, (30, 30, 30))
                    Window.blit(render, (10, startY + (33 * i)))
                    break
            timer += 1
        else:
            set_state(f"wstory{currentIndexstr}")
    elif State[0:6] == "wstory":
        Framerate = 60
        currentIndexstr = State[-1:]
        if timer < 360:

            timer += 1
        else:
            if currentIndexstr != "5":
                set_state(f"story{str(int(currentIndexstr)+1)}")
            else:
                set_state("fadeOutStory")

    # THE ACTUAL GAME (to whoever's reading the source code I apologize for this monstrosity)
    elif State == "gameplaying":
        foodCooldown += 1
        Window.blit(gamebg, (0, 0))
        render_jesus()
        #add random person
        if rollForPerson():
            if random.randint(1, 2) == 1:
                people.append(classes.Person("B"))
            else:
                people.append(classes.Person("F"))

        #render people
        for index, person in enumerate(people):
            if person.state == "Walking":
                person.x = person.x + 5
                if person.x == person.targetx:
                    person.state = "Waiting"
            elif person.state == "Waiting":
                person.currTimer += 1
                if person.currTimer == person.waitTime:
                    person.state = "Loss"
                    lives -= 1
            elif person.state == "Loss" or person.state == "Receive":
                person.x = person.x + 5
                if person.x > 900:
                    people.pop(index)
            personimage = pygame.image.load(addPath(f"personsprites/{person.type}{person.state}M.png"))
            prect = personimage.get_rect()
            prect.center = (person.x, person.y)
            Window.blit(personimage, prect)


        #render foods
        for index, food in enumerate(foods):
            image = pygame.image.load(addPath(f"{food.type}.png"))
            imgrect = image.get_rect()
            imgrect.center = (food.x, food.y)
            Window.blit(image, imgrect)
            food.y = food.y + 7

            for otherindex, person in enumerate(people):
                if person.state != "Waiting":
                    continue
                if imgrect.colliderect(pygame.Rect(person.x, person.y, 120, 180)):
                    if person.type == food.type[:1].upper():
                        person.state = "Receive"
                        foods.pop(index)
                        score += 1
                        break

            if food.y > 550:
                lives -= 1
                foods.pop(index)

        #render score and other data
        Window.blit(scoreFont.render(f"Score: {str(score)}", True, (30, 30, 30)), (5, 10))
        #temp lives display
        Window.blit(scoreFont.render(f"Lives: {str(lives)}", True, (30, 30, 30)), (5, 30))
        timer += 1
        if lives == 0:
            set_state("loss")
    elif State == "loss":
        if timer < 300:
            textSurface = finalscreenFont.render(f"Final Score: {str(score)}", True, (30, 30, 30))
            tsrect = textSurface.get_rect()
            tsrect.center = (400, 350)
            bigtext = finalscreenlostFont.render("You Lost!", True, (30, 30, 30))
            btsRect = bigtext.get_rect()
            btsRect.center = (400, 275)
            Window.blit(textSurface, tsrect)
            Window.blit(bigtext, btsRect)
            timer += 1
        else:
            set_state("backtomenu")
    elif State == "backtomenu":
        if timer < 30:
            fade_game(False)
        else:
            set_state("loadMain")
    pygame.display.flip()
    Clock.tick(Framerate)