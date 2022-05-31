"""
BlackJack 2.0 - with pygame module
No "split" function
"""
import time
import random
import pygame as p


def load_images(cards):
    """Initialize a global dictionary of images. This will be called exactly once"""
    for card in cards:
        IMAGES[card] = p.transform.scale(p.image.load(
            "images/" + card + ".png"), (100, 145))


all_cards = ["2C", "2D", "2H", "2S",
             "3C", "3D", "3H", "3S",
             "4C", "4D", "4H", "4S",
             "5C", "5D", "5H", "5S",
             "6C", "6D", "6H", "6S",
             "7C", "7D", "7H", "7S",
             "8C", "8D", "8H", "8S",
             "9C", "9D", "9H", "9S",
             "10C", "10D", "10H", "10S",
             "JC", "JD", "JH", "JS",
             "QC", "QD", "QH", "QS",
             "KC", "KD", "KH", "KS",
             "AC", "AD", "AH", "AS", "Unknown"
             ]
card_values = {"2C": 2, "2D": 2, "2H": 2, "2S": 2,
               "3C": 3, "3D": 3, "3H": 3, "3S": 3,
               "4C": 4, "4D": 4, "4H": 4, "4S": 4,
               "5C": 5, "5D": 5, "5H": 5, "5S": 5,
               "6C": 6, "6D": 6, "6H": 6, "6S": 6,
               "7C": 7, "7D": 7, "7H": 7, "7S": 7,
               "8C": 8, "8D": 8, "8H": 8, "8S": 8,
               "9C": 9, "9D": 9, "9H": 9, "9S": 9,
               "10C": 10, "10D": 10, "10H": 10, "10S": 10,
               "JC": 10, "JD": 10, "JH": 10, "JS": 10,
               "QC": 10, "QD": 10, "QH": 10, "QS": 10,
               "KC": 10, "KD": 10, "KH": 10, "KS": 10,
               "AC": 11, "AD": 11, "AH": 11, "AS": 11, "Unknown": 0
               }

cards = list(all_cards)
cards.remove("Unknown")
WIDTH = 800
HEIGHT = 512
MAX_FPS = 15
IMAGES = {}
user_cards = []
dealer_cards = []
p.init()
screen = p.display.set_mode((WIDTH, HEIGHT))
screen.fill(p.Color("black"))
load_images(all_cards)
sound_deal_card = p.mixer.Sound("sounds/deal_card.mp3")
bank = 100
bet = 10


def deal_card(card_pool):
    """Returns a random card from the deck"""
    card = random.choice(card_pool)
    cards.remove(card)
    p.mixer.Sound.play(sound_deal_card)
    return card


def calculate_score(cards, card_values):
    """Returns a score from a list of cards"""
    values = []
    for card in cards:
        values.append(card_values.get(card))
    if 11 in values:
        for value in values:
            if sum(values) > 21 and value == 11:
                values[values.index(value)] = 1
    return sum(values)


def result(user_score, dealer_score, user_cards, dealer_cards):
    """Compares scores and returns winner on the screen"""
    global bank
    if user_score == 21 and len(user_cards) == 2:
        if dealer_score == 21 and len(dealer_score) == 2:
            winner = "Draw - BlackJacks"
            color = (0, 0, 255)
        else:
            winner = "You have BlackJack!"
            color = (0, 255, 0)
            bank += bet
    elif dealer_score == 21 and len(dealer_cards) == 2:
        winner = "Dealer has BlackJack!"
        color = (255, 0, 0)
        bank -= bet
    elif user_score == dealer_score:
        winner = "Draw"
        color = (0, 0, 255)
    elif dealer_score > 21:
        winner = "You have won!"
        color = (0, 255, 0)
        bank += bet
    elif user_score > 21:
        winner = "You have lost!"
        color = (255, 0, 0)
        bank -= bet
    elif user_score > dealer_score:
        winner = "You have won!"
        color = (0, 255, 0)
        bank += bet
    else:
        winner = "You have lost"
        color = (255, 0, 0)
        bank -= bet

    font = p.font.SysFont("comicsans", 30, bold=True)
    label = font.render(f"{winner}", 1, color, (0, 0, 0))
    screen.blit(label, (
        (300 + 420 + 105) // 2 - label.get_width() // 2, HEIGHT - 150))
    font = p.font.SysFont("comicsans", 20)
    label_play_again = font.render(
        "Click to play again", 1, (255, 255, 255), (0, 0, 0))
    screen.blit(label_play_again, (
        (300 + 420 + 105) // 2 - label_play_again.get_width() // 2, HEIGHT - 40))


def dealer_needs_draw(user_score, dealer_score):
    "Returns True, if dealer needs to draw to not lose"
    if dealer_score == 0 or user_score == 0:
        return False
    if dealer_score >= 17:
        return False
    return True


def draw_dealer_cards(dealer_cards):
    for card in dealer_cards:
        row = dealer_cards.index(card) // 3
        col = dealer_cards.index(card) % 3
        screen.blit(IMAGES[card], p.Rect(
            500 + 50 * (col), 100 + 50 * (row), IMAGES[card].get_width(), IMAGES[card].get_height()))


def draw_user_cards(user_cards):
    for card in user_cards:
        row = user_cards.index(card) // 3
        col = user_cards.index(card) % 3
        screen.blit(IMAGES[card], p.Rect(
            200 + 50 * (col), 100 + 50 * (row), IMAGES[card].get_width(), IMAGES[card].get_height()))


def draw_buttons():
    font = p.font.SysFont("comicsans", 30)
    label = font.render("Draw", 1, (255, 255, 255))
    label2 = font.render("Stand", 1, (255, 255, 255))
    p.draw.rect(screen, (255, 255, 255), p.Rect(300, HEIGHT - 100, 105, 50), 2)
    p.draw.rect(screen, (255, 255, 255), p.Rect(420, HEIGHT - 100, 105, 50), 2)
    screen.blit(label, (315, HEIGHT - 100))
    screen.blit(label2, (430, HEIGHT - 100))


def draw_text(user_score, dealer_score):
    if bank > 100:
        color = (0, 255, 0)
    elif bank <= 50:
        color = (255, 0, 0)
    else:
        color = (255, 255, 255)
    p.display.set_caption("BlackJack v2.0")
    font = p.font.SysFont("comicsans", 40, bold=True)
    label = font.render(f"{user_score}", 1, (0, 255, 0), (0, 0, 0))
    label2 = font.render(f"{dealer_score}", 1, (255, 0, 0), (0, 0, 0))
    screen.blit(label, (200, 30))
    screen.blit(label2, (500, 30))
    font2 = p.font.SysFont("comicsans", 30, bold=True)
    label_bank = font2.render(f"bank: {bank}", 1, color, (0, 0, 0))
    screen.blit(label_bank, (30, HEIGHT - 100))
    label_bet = font2.render(f"bet: {bet}", 1, (255, 255, 255), (0, 0, 0))
    screen.blit(label_bet, (30, HEIGHT - 60))


def draw_gamestate(user_score, dealer_score):
    draw_dealer_cards(dealer_cards)
    draw_user_cards(user_cards)
    draw_buttons()
    draw_text(user_score, dealer_score)


def main():
    global user_cards, dealer_cards, cards
    play = True
    while play:
        screen.fill(p.Color("black"))
        user_cards = []
        dealer_cards = []
        cards = list(all_cards)
        cards.remove("Unknown")

        for i in range(2):
            user_cards.append(deal_card(cards))
            user_score = calculate_score(user_cards, card_values)
            dealer_score = calculate_score(dealer_cards, card_values)
            draw_gamestate(user_score, dealer_score)
            p.display.flip()
            time.sleep(0.6)
            if i == 0:
                dealer_cards.append(deal_card(cards))
            else:
                dealer_cards.append("Unknown")
                unknown = deal_card(cards)
            dealer_score = calculate_score(dealer_cards, card_values)
            draw_gamestate(user_score, dealer_score)
            p.display.flip()
            time.sleep(0.6)

        user_score = calculate_score(user_cards, card_values)
        dealer_score = calculate_score(dealer_cards, card_values)
        draw_gamestate(user_score, dealer_score)
        p.display.flip()
        running = True

        while running:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                    play = False
                elif e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()    # (x, y) location of the mouse
                    if 300 <= location[0] <= 405 and HEIGHT - 100 <= location[1] <= HEIGHT - 50:
                        user_cards.append(deal_card(cards))
                        user_score = calculate_score(user_cards, card_values)
                        if user_score > 21:
                            if "Unknown" in dealer_cards:
                                dealer_cards.remove("Unknown")
                                dealer_cards.append(unknown)
                                dealer_score = calculate_score(
                                    dealer_cards, card_values)
                            running = False
                        draw_gamestate(user_score, dealer_score)
                        p.display.flip()
                    elif 420 <= location[0] <= 525 and HEIGHT - 100 <= location[1] <= HEIGHT - 50:
                        if "Unknown" in dealer_cards:
                            dealer_cards.remove("Unknown")
                            dealer_cards.append(unknown)
                            p.mixer.Sound.play(sound_deal_card)
                            dealer_score = calculate_score(
                                dealer_cards, card_values)
                            draw_gamestate(user_score, dealer_score)
                            p.display.flip()
                            time.sleep(1)
                        while dealer_needs_draw(user_score, dealer_score):
                            dealer_cards.append(deal_card(cards))
                            dealer_score = calculate_score(
                                dealer_cards, card_values)
                            draw_gamestate(user_score, dealer_score)
                            p.display.flip()
                            time.sleep(0.5)
                        running = False
        screen.fill(p.Color("black"))
        result(user_score, dealer_score, user_cards, dealer_cards)
        draw_gamestate(user_score, dealer_score)
        p.display.flip()

        if play != False:
            wait = True
        while wait:
            for e in p.event.get():
                if e.type == p.QUIT:
                    wait = False
                    play = False
                elif e.type in (p.KEYDOWN, p.MOUSEBUTTONDOWN):
                    wait = False


main()
