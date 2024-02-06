import requests
from src import cards as card_art
from time import sleep


class Deck:

    def __init__(self):
        Deck.id = None

    def new_deck():
        new_deck_url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6"
        new_deck_response = requests.get(new_deck_url)
        new_deck_data = (
            new_deck_response.json()
            if new_deck_response and new_deck_response.status_code == 200
            else None
        )

        Deck.id = new_deck_data.get("deck_id")

    def draw_card():
        card_url = f"https://deckofcardsapi.com/api/deck/{Deck.id}/draw/?count=2"
        card_url_response = requests.get(card_url)
        card_data = (
            card_url_response.json()
            if card_url_response and card_url_response.status_code == 200
            else None
        )
        card = card_data.get("cards")[0]["code"]
        value = card_data.get("cards")[0]["value"]
        if value == "ACE":
            value = 11
        if value == "KING":
            value = 10
        if value == "QUEEN":
            value = 10
        if value == "JACK":
            value = 10
        return card, int(value)


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.values = []
        self.total = 0
        self.art = []

    def deal(self):
        card1 = Deck.draw_card()
        card2 = Deck.draw_card()
        self.hand.append(card1[0])
        self.hand.append(card2[0])
        self.values.append(card1[1])
        self.values.append(card2[1])
        self.tally()

    def tally(self):
        total = 0
        for value in self.values:
            total = total + value
        self.total = total

    def hit(self):
        card = Deck.draw_card()
        self.hand.append(card[0])
        self.values.append(card[1])
        self.tally()

    def get_art(self):
        art = []
        for card in self.hand:
            # print(card)
            value = card[0]
            suit = card[1]
            if suit == "H":
                art.append(card_art.hearts[value])
            if suit == "D":
                art.append(card_art.diamonds[value])
            if suit == "C":
                art.append(card_art.clubs[value])
            if suit == "S":
                art.append(card_art.spades[value])
        for card in art:
            self.art.append(card)


class Game:

    dealer = Player("DEALER")

    def get_name():
        player_name = input("What's your name? ")
        player = Player(player_name)
        return player

    def new_game():
        Deck.new_deck()
        player.deal()
        player.get_art()
        for card in player.art:
            print(card)
        Game.dealer.deal()
        Game.dealer.get_art()
        print(f"{card_art.blank}\n{Game.dealer.art[1]}")
        while True:
            if player.total == 21:
                return False
            if player.total > 21:
                if 11 in player.values:
                    player.total = player.total - 10
                else:
                    return False
                print(player.total)
            else:
                hit_confirm = input("Hit? [y/n] ")
                if hit_confirm == "y":
                    print(f"{player.name} hits.\n")
                    player.hit()
                else:
                    print(f"{player.name} stands.\n\nDealer turn: \n")
                    return False

    def dealer_turn():
        while True:
            if Game.dealer.total > 21:
                return False
            if Game.dealer.total == 21:
                return False
            if Game.dealer.total < 21:
                if Game.dealer.total < 18:
                    print(f"{Game.dealer.name}: hit me!\n")
                    Game.dealer.hit()
                    print(f"{Game.dealer.hand[-1]}\n")
                if Game.dealer.total > 17:
                    return False

    def declare_winner():
        player_total = player.total
        dealer_total = Game.dealer.total
        if player_total > dealer_total:
            winner = print(
                f"{Game.dealer.name}: {Game.dealer.hand} Total: {dealer_total}\n{player.name}: {player.hand} Total: {player_total}\n{player.name} wins!"
            )
            return winner
        if dealer_total > player_total:
            winner = print(
                f"{Game.dealer.name}: {Game.dealer.hand} Total: {dealer_total}\n{player.name}: {player.hand} Total: {player_total}\n{Game.dealer.name} wins!"
            )
            return winner
        if dealer_total == player_total:
            winner = print(
                f"{Game.dealer.name}: {Game.dealer.hand} Total: {dealer_total}\n{player.name}: {player.hand} Total: {player_total}\nTie - split the pot!"
            )
            return winner


if __name__ == "__main__":
    player = Game.get_name()
    Game.new_game()
    Game.dealer_turn()
    Game.declare_winner()
