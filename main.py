import pygame
import time
import random
import math


class Card(pygame.sprite.Sprite):
    def __init__(self, x, y, magic_nubmer, front):
        super(self.__class__, self).__init__()
        self.image = pygame.image.load('card-back (1).png').convert()
        self.front = pygame.image.load(front).convert()
        self.image.set_colorkey(red_to_ignore)
        self.front.set_colorkey(red_to_ignore)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.switched = False  # determines whether 'front' and 'image' switch, that is- card shown.
        self.magic_number = magic_nubmer

    def get_pos(self):
        return self.rect.x, self.rect.y


def draw(cards):
    for i in range(len(cards)):
        display.blit(cards[i].image, cards[i].get_pos())

    for mouse in mouse_list:
        display.blit(card_image, mouse)


def show_card(card):
    display.blit(card.front, card.get_pos())
    temp = card.image
    card.image = card.front
    card.front = temp
    card.switched = True
    pygame.display.flip()


def score(score, wins):
    value = score_font.render(f"Your score: {score}", True, score_color)
    display.blit(value, [5, 0])
    v = score_font.render(f"Memory Card Game", True, title_color)
    display.blit(v, [250, 50])
    w = score_font.render(f"Wins: {wins}", True, green)
    display.blit(w, [670, 0])


def check_shown_cards(shown,card_list):
    if shown[0].magic_number == shown[1].magic_number:
        for c in card_list:
            if c.switched:
                card_list.remove(c)
        return True
    return False


def hide_cards(card_list):
    time.sleep(0.5)
    for c in card_list:
        if c.switched:
            temp = c.image
            c.image = c.front
            c.front = temp
            c.switched = False
    # draw(card_list)


pygame.init()

# colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (59, 168, 96)
blue = (50, 153, 213)
back_color = (239, 239, 239)
score_color = (255, 209, 103)
title_color = (119, 0, 21)
red_to_ignore = (237, 28, 36)
score_font = pygame.font.SysFont("comicsansms", 35)
font_style = pygame.font.SysFont("bahnschrift", 23)

# dimensions
WIDTH = 800
HEIGHT = 600
DIMENSIONS = (WIDTH, HEIGHT)
display = pygame.display.set_mode(DIMENSIONS)
pygame.display.set_caption("Bali's memory game")
card_width = 100
card_length = 133

# location
# x = 40
# y = 230
x_change = 0
y_change = 0
space_between_cards = 150
mouse_list = []

# mouse events
LEFT = 1
SCROLL = 2
RIGHT = 3

# global vars
fronts = ['2.png', '3.png', '4.png', '5.png', 'A.png']
# card_list = []

clock = pygame.time.Clock()

card_image = pygame.image.load('card-back (1).png').convert()
card_image.set_colorkey(red_to_ignore)

wins = 0

def generate_cards(card_list):
    y=230
    for i in range(2):
        x = 40
        random.shuffle(fronts)
        for j in range(5):
            front = fronts[j]
            number = 0
            if front == '2.png':
                number = 2

            if front == '3.png':
                number = 3

            if front == '4.png':
                number = 4

            if front == '5.png':
                number = 5

            if front == 'A.png':
                number = 1

            card_list.append(Card(x, y, number, front=front))
            x = x + space_between_cards
        y = y + 190

def message(msg, colour, dim=None, font=font_style):
    if dim is None:
        dim = [WIDTH / 5, HEIGHT / 3]
    mesg = font.render(msg, True, colour)
    display.blit(mesg, dim)
    pygame.display.flip()
    time.sleep(0.5)

def game(wins):
    y = 230
    card_list = []
    # init card list
    generate_cards(card_list)

    shown_cards = []
    my_score = 0
    game_on = True
    game_end = False
    while game_on:
        if len(card_list) == 1:
            game_end = True

        while game_end:
            display.fill(back_color)
            message("You have won! Press R to restart or Q to quit", red)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_on = False
                        pygame.quit()
                    if event.key == pygame.K_r:
                        wins = wins + 1
                        game(wins)

        if len(shown_cards) == 2:
            if not len(card_list) == 1:
                if check_shown_cards(shown_cards,card_list):
                    my_score = my_score + 10
                    message("Correct!", green, dim=[330, 150], font=score_font)
                    pygame.display.flip()
                else:
                    message("Try Again!", (237,57,20), dim=[310, 150], font=score_font)
                    pygame.display.flip()
                hide_cards(card_list)
                shown_cards = []

        display.fill(back_color)

        draw(card_list)
        score(my_score,wins)

        mouse_p = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                for card in card_list:
                    if card.rect.collidepoint(mouse_p):
                        if not card.switched:
                            if len(shown_cards) < 2:
                                shown_cards.append(card)
                                show_card(card)
                            else:
                                break
                        else:
                            message("Can't choose the same card!", title_color, [190, 150], font=score_font)

        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    quit()

game(wins)