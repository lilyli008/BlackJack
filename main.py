import FreeSimpleGUI as sg
import time
from poker import *


# Game setup
deck = Deck()
deck.shuffle()
player=Player()

font_choice=("Helvetica", 10, "bold italic")
font_choice_result=("Helvetica", 15, "bold italic")
bold_font = ("Helvetica", 10, "bold")
background_image = "BlackJack.png"

layout = [
    [sg.Text('Blackjack Game', size=(15, 1), justification='left', font='Helvetica 20'),
     sg.Image(filename=background_image,subsample=6,key="-BACKGROUND-",size=(180,150))],
    [sg.Text(f"Total Balance($):",size=(15,1)),sg.Text(f"${player.total}",key="-TOTAL-",font=font_choice_result),
     sg.Text('Enter Your Bet ($):'),
     sg.InputText('100', key='-BET-', size=(10, 1))],
         [sg.Text('You bet: ',key="-BET-OUTPUT",size=(15,1),font=font_choice),
          sg.Button("Bet the Game",key="Start"),sg.Text(key="Round",font=bold_font)],
    [sg.Text('Dealer\'s Cards:', size=(15, 1)),
     sg.Text(key='-DEALER-', size=(25, 5),background_color='black',font=font_choice),
     sg.Text("Values:"),sg.Text(key='-DEALER-VALUE-',font=font_choice_result)],
    [sg.Text('Player\'s Cards:', size=(15, 1)),
     sg.Text(key='-PLAYER-', size=(25, 5),background_color='black',font=font_choice),
     sg.Text("Values:"),sg.Text("",key='-PLAYER-VALUE-',font=font_choice_result)],
    [sg.Button('Hit',disabled=True), sg.Button('Stand',disabled=True), sg.Button('Quit')],
    [sg.Text('Result:', size=(15, 1),font=font_choice), sg.Text('', key='-RESULT-', size=(13, 1),
                                               font=font_choice_result,text_color="Yellow"),
     sg.Text('', key='value_change',
             font=font_choice_result, text_color="Yellow"),sg.Image(key="win_pic")
     ]
]

# Create the window
window = sg.Window('Blackjack', layout,resizable=True)

# Event loop

round=1
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break

    if event=="Start":
        window["Round"].update(f"Round {round}")
        bet_value = float(values["-BET-"])

        if bet_value>player.total:
            sg.popup("You cannot place a bet exceeding your current balance.")
            continue

        window["-BET-OUTPUT"].update(f"You bet: ${bet_value}")

        player_hand = Hand()
        dealer_hand = Hand()
        window['Hit'].update(disabled=False)
        window['Stand'].update(disabled=False)
        window['-RESULT-'].update("")
        window['value_change'].update("")
        # Initial dealing
        for _ in range(2):
            player_hand.add_card(deck.deal())
            dealer_hand.add_card(deck.deal())

        time.sleep(0.5)
        window["-DEALER-"].update(f'{dealer_hand.cards[0]}\n <hidden>')
        window["-DEALER-VALUE-"].update(dealer_hand.cards[0].value)
        window["-PLAYER-"].update(str(player_hand))
        window["-PLAYER-VALUE-"].update(player_hand.value)
        window["Start"].update(disabled=True)
        window["win_pic"].update("")

        if player_hand.value==21:
            window['Hit'].update(disabled=True)
            event='Stand'

    if event == 'Hit':
        # Player hits, draw a card
        player_hand.add_card(deck.deal())
        window['-PLAYER-'].update(str(player_hand))
        window['-PLAYER-VALUE-'].update(player_hand.value)
        if player_hand.value>=21:
            window['Hit'].update(disabled=True)
            event='Stand'

    if event == 'Stand':
        # Dealer's turn: dealer hits until reaching 17
        if player_hand.value<=21:
            while dealer_hand.value < 17:
                dealer_hand.add_card(deck.deal())

        # Show dealer's cards and check for winner
        window['-DEALER-'].update(str(dealer_hand))
        window['-DEALER-VALUE-'].update(dealer_hand.value)
        result = check_for_winner(player_hand, dealer_hand)
        window['-RESULT-'].update(result[0])
        player.balance_update(result[1], bet_value)
        window['-TOTAL-'].update(player.total)
        if player.total <= 0:
            sg.popup("Your balance is zero.We hope to see you again soon!")
            break
        window['Hit'].update(disabled=True)
        window['Stand'].update(disabled=True)
        if result[1]=="BJ":
            window['value_change'].update(f"+${bet_value*1.5}")
            window['win_pic'].update(sg.EMOJI_BASE64_HAPPY_THUMBS_UP)
        elif result[1] == "win":
            window['value_change'].update(f"+${bet_value}")
            window['win_pic'].update(sg.EMOJI_BASE64_HAPPY_HEARTS)
        elif result[1] == "lose":
            window['value_change'].update(f"-${bet_value}")
            window['win_pic'].update(sg.EMOJI_BASE64_SAD)
        window["Start"].update(disabled=False)
        round+=1
        #break

window.close()
