import random

# Define the deck, suits, and ranks
suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
card_values = {'Two': 2, 'Three': 3, 'Four': 4,
          'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}

# Card and Deck classes
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value=card_values[self.rank]

    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards)==1:
            self.__init__()
            self.shuffle()
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)


# Hand class
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += card_values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
        self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def __str__(self):
        return '\n'.join([str(card) for card in self.cards])



class Player:
    def __init__(self, total=1000):
        self.total = total

    def balance_update(self, win, bet):
        if win=="BJ":
            self.total += 1.5*bet
        elif win=="win":
            self.total += bet
        elif win=="lose":
            self.total -= bet
        else:
            pass

# Function to check for a winner
def check_for_winner(player_hand, dealer_hand):
    if player_hand.value==21 and len(player_hand.cards)==2:
        return "Black Jack","BJ"
    elif player_hand.value > 21:
        return "Player busts! ","lose"
    elif dealer_hand.value > 21:
        return "Dealer busts!","win"
    elif player_hand.value > dealer_hand.value:
        return "Player wins!","win"
    elif player_hand.value < dealer_hand.value:
        return "Player loses!","lose"
    else:
        return "It's a tie!","tie"

if __name__=="__main__":
    deck=Deck()

    for i in range(50):
        deck.deal()
        print(len(deck))