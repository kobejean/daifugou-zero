
class Card:
    """Card class."""
    SPADE = 0
    HEART = 1
    DIAMOND = 2
    CLUB = 3
    JOKER = 4

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def beats(self, card2, is_reversed):
        if (self.suit == self.JOKER or card2.suit == self.JOKER):
            # 3 conditions: self is jk, card2 is jk or both
            # if card2 is not jk then self must be jk and so self beats card2
            return (card2.suit != self.JOKER)
        elif (not is_reversed):
            return self > card2
        else:
            return self < card2

    def is_special(self):
        return (self.suit == self.JOKER or self.value in [8, 10, 11])

    def __gt__(self, card2):
        if (self.suit == self.JOKER or card2.suit == self.JOKER):
            return (card2.suit != self.JOKER)
        else:
            # convert to normal scale so that 3->0, 10->7, 2->12 ect.
            # because 3 is lowest and 2 is highest
            norm1 = ((self.value - 3) % 13) + 1
            norm2 = ((card2.value - 3) % 13) + 1
            return norm1 > norm2

    def __lt__(self, card2):
        if (self.suit == self.JOKER or card2.suit == self.JOKER):
            return (card2.suit == self.JOKER)
        else:
            # convert to normal scale so that 3->0, 10->7, 2->12 ect.
            # because 3 is lowest and 2 is highest
            norm1 = ((self.value - 3) % 13) + 1
            norm2 = ((card2.value - 3) % 13) + 1
            return norm1 < norm2

    def __ge__(self, card2):
        return not (self < card2)

    def __le__(self, card2):
        return not (self > card2)

    def text(self):
        text = "🂠🂡🂢🂣🂤🂥🂦🂧🂨🂩🂪🂫🂭🂮🂱🂲🂳🂴🂵🂶🂷🂸🂹🂺🂻🂽🂾🃁🃂🃃🃄🃅🃆🃇🃈🃉🃊🃋🃍🃎🃑🃒🃓🃔🃕🃖🃗🃘🃙🃚🃛🃝🃞🃟"
        if (self.suit == self.JOKER):
            return text[53]
        else:
            idx = int(self.suit) * 13 + self.value
            return text[idx]

    def cards_by_value_count(cards, value):
        count = 0
        for card in cards:
            if card.value == value:
                count += 1

    def cards_are_playable(prev_cards, new_cards, is_reversed, is_first_move):
        if new_cards:
            new_cards.sort()

            # check if all have same value or joker
            value = new_cards[0].value

            for card in new_cards:
                # if not same value and not joker (value 0)
                if card.value != value and card.value != 0:
                    print("not same value and not joker")
                    return False

            if prev_cards:
                prev_cards.sort()
                # if playing on top
                # must match size ex. single, double triple ect.
                if len(prev_cards) != len(new_cards):
                    print("size doesn't match")
                    return False
                if new_cards[0].beats(prev_cards[0], is_reversed):
                    return True
                else:
                    return False

            elif(is_first_move):
                # must be start of game
                found_diamond = False
                for card in new_cards:
                    if card.value != 3: return False
                    if card.suit == Card.DIAMOND: found_diamond = True
                return found_diamond
            else:
                # starting new pile
                return True
        else:
            return False
