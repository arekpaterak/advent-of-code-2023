from __future__ import annotations
from enum import Enum, auto
from functools import total_ordering

import sys
from dataclasses import dataclass


INPUTS = ["input.txt", "example.txt"]


@total_ordering
class Card(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    T = 10
    J = 0
    Q = 12
    K = 13
    A = 14

    @classmethod
    def from_str(cls, card: str) -> Card:
        if card.isdigit():
            return cls(int(card))
        elif card == "T":
            return cls.T
        else:
            return cls[card.upper()]

    def __lt__(self, obj):
        return self.value < obj.value

    def __repr__(self) -> str:
        if self.value < 10:
            return str(self.value)
        else:
            return self.name

    def __str__(self) -> str:
        if self.value < 10:
            return str(self.value)
        else:
            return self.name


@total_ordering
class HandType(Enum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIRS = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()

    @classmethod
    def from_cards(cls, cards: list[Card]) -> HandType:
        card_counts = {card: cards.count(card) for card in cards}

        joker_count = card_counts.get(Card.J, 0)

        card_counts_without_jokers = {
            card: count for card, count in card_counts.items() if card != Card.J
        }

        match joker_count:
            case 5:
                return cls.FIVE_OF_A_KIND
            case 4:
                return cls.FIVE_OF_A_KIND
            case 3:
                if 2 in card_counts_without_jokers.values():
                    return cls.FIVE_OF_A_KIND
                else:
                    return cls.FOUR_OF_A_KIND
            case 2:
                if 3 in card_counts_without_jokers.values():
                    return cls.FIVE_OF_A_KIND
                elif 2 in card_counts_without_jokers.values():
                    return cls.FOUR_OF_A_KIND
                else:
                    return cls.THREE_OF_A_KIND
            case 1:
                if 4 in card_counts_without_jokers.values():
                    return cls.FIVE_OF_A_KIND
                elif 3 in card_counts_without_jokers.values():
                    return cls.FOUR_OF_A_KIND
                elif 2 in card_counts_without_jokers.values():
                    if list(card_counts.values()).count(2) == 2:
                        return cls.FULL_HOUSE
                    else:
                        return cls.THREE_OF_A_KIND
                else:
                    return cls.ONE_PAIR
            case 0:
                if 5 in card_counts.values():
                    return cls.FIVE_OF_A_KIND
                elif 4 in card_counts.values():
                    return cls.FOUR_OF_A_KIND
                elif 3 in card_counts.values():
                    if 2 in card_counts.values():
                        return cls.FULL_HOUSE
                    else:
                        return cls.THREE_OF_A_KIND
                elif 2 in card_counts.values():
                    if list(card_counts.values()).count(2) == 2:
                        return cls.TWO_PAIRS
                    else:
                        return cls.ONE_PAIR
                else:
                    return cls.HIGH_CARD

    def __lt__(self, obj):
        return self.value < obj.value

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name


@total_ordering
@dataclass
class Hand:
    cards: list[Card]
    hand_type: HandType
    bid: int

    @classmethod
    def from_input(cls, line: str) -> Hand:
        cards, bid = line.split(" ")

        cards = [Card.from_str(card) for card in cards]
        hand_type = HandType.from_cards(cards)
        bid = int(bid)

        return cls(cards, hand_type, bid)

    def __lt__(self, obj):
        if self.hand_type != obj.hand_type:
            return self.hand_type < obj.hand_type
        else:
            for card, obj_card in zip(self.cards, obj.cards):
                if card != obj_card:
                    return card < obj_card
            else:
                return False

    def __gt__(self, obj):
        if self.hand_type != obj.hand_type:
            return self.hand_type > obj.hand_type
        else:
            for card, obj_card in zip(self.cards, obj.cards):
                if card != obj_card:
                    return card > obj_card
            else:
                return False

    def __le__(self, obj):
        if self.hand_type != obj.hand_type:
            return self.hand_type <= obj.hand_type
        else:
            for card, obj_card in zip(self.cards, obj.cards):
                if card != obj_card:
                    return card <= obj_card
            else:
                return True

    def __ge__(self, obj):
        if self.hand_type != obj.hand_type:
            return self.hand_type >= obj.hand_type
        else:
            for card, obj_card in zip(self.cards, obj.cards):
                if card != obj_card:
                    return card >= obj_card
            else:
                return True

    def __eq__(self, obj):
        if self.hand_type != obj.hand_type:
            return False
        else:
            for card, obj_card in zip(self.cards, obj.cards):
                if card != obj_card:
                    return False
            else:
                return True

    def __repr__(self):
        return (
            f"{''.join([str(card) for card in self.cards])} {self.hand_type} {self.bid}"
        )


if __name__ == "__main__":
    input_file_index = sys.argv[1]
    input_file = INPUTS[int(input_file_index)]

    with open(input_file) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    hands = [Hand.from_input(line) for line in lines]

    sorted_hands = sorted(hands)

    print("--- Part Two ---")
    total_winnings = sum(
        [rank * hand.bid for rank, hand in enumerate(sorted_hands, start=1)]
    )
    print("Answer:")
    print(total_winnings)
