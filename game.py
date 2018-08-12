import numpy as np
from random import shuffle

from card import Card
from player import Player

class Game:
    """game class."""
    def __init__(self, player_count):
        self.players = [Player() for i in range(player_count)]
        self.winners = []
        self.loosers = []
        self.current_cards = []
        self.history = []
        self.current_player = None
        self.current_player_num = 0
        self.pass_count = 0
        self.is_first_move = True
        self.is_reversed = False

    def create_deck(self):
        j1 = Card(Card.JOKER, 0)
        j2 = Card(Card.JOKER, 0)
        full_deck = [j1, j2]
        for suit in range(4):
            for value in range(1,14):
                full_deck.append(Card(suit, value))
        return full_deck

    def deal_out(self):
        full_deck = self.create_deck()
        shuffle(full_deck)
        for i in range(len(full_deck)):
            card = full_deck[i]
            j = i % len(self.players)
            self.players[j].deck.append(card)

    def sort_cards(self):
        for player in self.players:
            player.deck.sort()

    def clear_pile(self):
        self.is_reversed = False
        self.current_cards = []
        self.current_player = self.players[self.current_player_num]

    def find_starter(self):
        """find who has the three of diamonds and start with him."""
        for player in self.players:
            for card in player.deck:
                if (card.value == 3 and card.suit == Card.DIAMOND):
                    self.current_player = player
                    print("{} starts".format(player.name))

    def next_turn(self):
        self.current_player_num += 1
        self.current_player_num %= len(self.players)
        self.current_player = self.players[self.current_player_num]

    def process_current_cards(self):
        assert len(self.current_cards) > 0, "no cards to process"
        value = self.current_cards[0].value

        self.pass_count = 0

        # check for 3 of diamond to mark off is_first_move
        if (value == 3):
            for card in self.current_cards:
                if card.suit == Card.DIAMOND:
                    self.is_first_move = False

        if (value == 8): # clear pile
            self.clear_pile()
            return

        elif (value == 10):
            prompt_text = "Choose cards: "
            chosen_cards = self.pick_cards(prompt_text, passable = False)

        elif (value == 11):
            self.is_reversed = True

        self.next_turn()

    def pick_cards(self, prompt_text, passable = True):
        chosen_cards = []
        num_str = "  ①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳"
        print("P ", end = '')
        self.print_cards(self.current_cards)
        print("S ", end = '')
        self.print_cards(chosen_cards)
        print("H ", end = '')
        self.print_cards(self.current_player.deck)
        print(num_str)

        choice = input(prompt_text)

        while (choice):
            if (choice == "p" and passable):
                self.pass_count += 1
                self.next_turn()
                return # for pass

            try:
                choice = int(choice)
                if (choice < 0):
                    undo_idx = choice * -1 - 1
                    try:
                        self.current_player.deck.append(chosen_cards.pop(undo_idx))
                    except IndexError:
                        print("error: idx out of range")
                else:
                    idx = choice - 1
                    try:
                        chosen_cards.append(self.current_player.deck.pop(idx))
                    except IndexError:
                        print("error: idx out of range")

            except ValueError:
                print("error: not integer")


            self.current_player.deck.sort()
            chosen_cards.sort()

            print("P ", end = '')
            self.print_cards(self.current_cards)
            print("S ", end = '')
            self.print_cards(chosen_cards)
            print("H ", end = '')
            self.print_cards(self.current_player.deck)
            print(num_str)

            choice = input(prompt_text)

        return chosen_cards

    def print_turn(self):
        # if everyone else passed clear pile
        if (self.pass_count == len(self.players) - 1):
            self.clear_pile()

        print("\n{}\'s turn!\n".format(self.current_player.name))
        input("\n\n\n\n")

        prompt_text = "Choose cards: "
        chosen_cards = self.pick_cards(prompt_text, passable = True)

        if (Card.cards_are_playable(self.current_cards, chosen_cards,
                                    self.is_reversed, self.is_first_move)):
            self.current_cards = chosen_cards
            self.history.append(chosen_cards)
            self.process_current_cards()
        elif (chosen_cards):
            print("Try again")
            self.current_player.deck.extend(chosen_cards)
            self.current_player.deck.sort()
            chosen_cards = []
            self.print_turn()

    def print_cards(self, cards):
        for card in cards:
            print(card.text(), end = '')
        print()

    def print_all(self):
        for player in self.players:
            for card in player.deck:
                print(card.text(), end = '')
            print()

    def check_for_win(self):
        for (i, player) in enumerate(self.players):
            if len(player.deck) == 0:
                assert self.history, "no history"
                if self.history[-1][0].is_special():
                    self.loosers.append(self.players.pop(i))
                    print("{} looses!".format(player.name))
                else:
                    self.winners.append(self.players.pop(i))
                    print("{} wins #{}!".format(player.name, len(self.winners)))

    def start(self):
        self.deal_out()
        self.sort_cards()
        self.find_starter()
        while self.players:
            self.print_turn()
            self.check_for_win()

        self.winners.extend(self.loosers)
        self.loosers = []
        print("Scoreboard")
        for (i, player) in enumerate(self.winners):
            print("#{} {}".format(i+1, player.name))



# try:
#     game = Game(int(input("How many players? ")))
#     for player in game.players:
#         player.name = input("Player name: ")
#     game.start()
# except ValueError:
#     print("Value error")

game = Game(3)
game.players[0].name = "Jean"
game.players[1].name = "Rick"
game.players[2].name = "Sachico"
game.start()
