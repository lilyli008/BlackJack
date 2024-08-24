from poker import *
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
#n=int(input("Enter the number of simulated round:"))
#balance=float(input("Enter the starting balance (bet=1):"))
#bet=1

deck=Deck()

def self_play():
    player_hand = Hand()
    dealer_hand = Hand()

    # Initial dealing
    for _ in range(2):
        player_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

    while player_hand.value < 17:
        player_hand.add_card(deck.deal())

    while dealer_hand.value < 17:
        dealer_hand.add_card(deck.deal())

    result=check_for_winner(player_hand, dealer_hand)
    return result

def self_play_strategy():
    player_hand = Hand()
    dealer_hand = Hand()

    # Initial dealing
    for _ in range(2):
        player_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

    while player_hand.value < 17:
        if player_hand.value<12:
            player_hand.add_card(deck.deal())
        elif dealer_hand.cards[0].value>=7:
            player_hand.add_card(deck.deal())
        else:
            break

    while dealer_hand.value < 17:
        dealer_hand.add_card(deck.deal())

    result=check_for_winner(player_hand, dealer_hand)
    return result


result_dict={}
result_dict["win percentage"]=[]
result_dict["tie percentage"]=[]
result_dict["lose percentage"]=[]
result_dict["total round"]=[]
result_dict["balance"]=[]

n_player=1000
max_round=10
initial_balance=10
player_bet=1

def autoplay(n_player=1000,max_round=100,straregy_func=self_play):
    for _ in range(n_player):
        n_win = 0
        n_tie = 0
        n_lose = 0
        balance=initial_balance
        bet=player_bet
        total_round=max_round
        for i in range(max_round):
            if balance<bet: #balance>2*initial_balance or
               total_round=i
               break
            else:
               result = straregy_func()

            if result[1]=='win' or result[1]=='BJ':
                n_win=n_win+1
                balance+=bet
            elif result[1]=='tie':
                n_tie=n_tie+1
            else:
                n_lose+=1
                balance=balance-bet

        win_pct=n_win/total_round
        tie_pct = n_tie / total_round
        lose_pct=n_lose/total_round
        result_dict["win percentage"].append(win_pct)
        result_dict["tie percentage"].append(tie_pct)
        result_dict["lose percentage"].append(lose_pct)
        result_dict["balance"].append(balance)
        result_dict["total round"].append(total_round)
    return result_dict

df_native=pd.DataFrame(autoplay())
print("Basic strategy:")
print(df_native.describe().loc["mean"])

df_strategy=pd.DataFrame(autoplay(straregy_func=self_play_strategy))
print("Advanced strategy:")
print(df_strategy.describe().loc["mean"])

NumberofPlay=np.linspace(10,200,20)
balance_result=[]
balance_result_strategy=[]
for x in NumberofPlay:
    df = pd.DataFrame(autoplay(straregy_func=self_play,max_round=int(x)))
    balance_result.append(df.describe().loc["mean", "balance"])
    df_strategy = pd.DataFrame(autoplay(straregy_func=self_play_strategy,max_round=int(x)))
    balance_result_strategy.append(df_strategy.describe().loc["mean", "balance"])


plt.plot(NumberofPlay,balance_result,marker='o',label='naive')
plt.plot(NumberofPlay,balance_result_strategy,marker='o',label='strategy')
plt.legend()
plt.show()

#final_output={}
#for key in result_dict:
#    final_output["Average "+key]=np.mean(result_dict[key])

# Print the final output in a nicer format
#print("Final Output:")
#for key, value in final_output.items():
#    if key=="Average total round":
#        print(f"{key}: {round(value,0)}")
#    elif key=="Average balance":
#        print (f"{key}: {round(value,2)}")
#    else:
#        print(f"{key}: {value*100:.2f}%")


#plt.hist(balance_lst,bins=10)
#print("winning percentage",round(np.mean(win_pct_lst),2))
#print("losing percentage",round(np.mean(lose_pct_lst),2))
#plt.show()

'''
print(lose_pct_lst)
plt.plot(trial_lst,win_pct_lst,marker='o',color='r')
plt.plot(trial_lst,lose_pct_lst,marker='o')
for i, txt in enumerate(lose_pct_lst):
    plt.annotate(round(txt,2), (trial_lst[i], lose_pct_lst[i]), textcoords="offset points", xytext=(0,10), ha='center')
for i, txt in enumerate(win_pct_lst):
    plt.annotate(round(txt,2), (trial_lst[i], win_pct_lst[i]), textcoords="offset points", xytext=(0,-12), ha='center')
plt.ylim([0,1])
plt.legend(["winning%",'losing%'],loc=1)
plt.show()
'''