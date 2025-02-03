import random

# Singapore Customized Blackjack Rules
# rules of my black jack game
# there is only one deck despite more players
# the third card which is A is 10
# you can choose to run or not play if cards are more than 15
# the dealer has his / her cards hidden
# the dealer can choose to open players' cards (they are originally hidden) after all the player's turn while her cards are hidden but if player exceeds 21 and the cards are opened by banker, player pays else bank pays if his/her points are lower
# if the player busts and banker bust, the player does not lose or gain
# if there are 5 cards in hand, the player must show his/her cards
# at any point of time, player/banker must have more than 15 points
# A can be 1 or 11
# blackjack is A + Q/J/K/10
# dealer plays last
# if dealer busts, no money  is gained or lost
# if banker busts, he/she pays to player who didnt

# Simulation parameters
num_simulations = 100000  # Number of simulated rounds

# Card deck (one deck of 52 cards)
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * \
    4  # Face cards count as 10, Ace as 11 initially

# Game-specific rules


def draw_card(deck):
    """Draws a random card from the deck."""
    return random.choice(deck)


def calculate_hand_value(hand):
    """Calculates the value of a hand, handling Aces as 1 or 11."""
    value = sum(hand)
    num_aces = hand.count(11)

    # Adjust for Aces if needed
    while value > 21 and num_aces:
        value -= 10  # Convert an Ace from 11 to 1
        num_aces -= 1
    return value


# Simulation results
player_wins = 0
banker_wins = 0
ties = 0
no_money_lost_or_gained = 0

for _ in range(num_simulations):
    # Reset deck each round
    current_deck = deck[:]

    # Deal initial hands (hidden)
    player_hand = [draw_card(current_deck), draw_card(current_deck)]
    banker_hand = [draw_card(current_deck), draw_card(current_deck)]

    # Apply the special rule for third Ace being 10
    if len(player_hand) == 3 and player_hand[-1] == 11:
        player_hand[-1] = 10

    # Player's turn: Player must have at least 15 to play, else they "run"
    if calculate_hand_value(player_hand) > 15:
        # Player decision: Hit until safe or bust
        # Random strategy
        while calculate_hand_value(player_hand) < 15 or (len(player_hand) < 5 and random.random() < 0.5):
            player_hand.append(draw_card(current_deck))
            if len(player_hand) == 3 and player_hand[-1] == 11:
                player_hand[-1] = 10  # Apply the third Ace rule

    # If the player busts, they only lose if banker chooses to reveal
    player_value = calculate_hand_value(player_hand)
    if player_value > 21:
        if random.random() < 0.5:  # 50% chance banker reveals bust
            banker_wins += 1
        else:
            no_money_lost_or_gained += 1
        continue

    # Banker's turn: Must have at least 15
    while calculate_hand_value(banker_hand) < 15:
        banker_hand.append(draw_card(current_deck))
        if len(banker_hand) == 3 and banker_hand[-1] == 11:
            banker_hand[-1] = 10  # Apply the third Ace rule

    banker_value = calculate_hand_value(banker_hand)

    # Determine winner based on final hand values
    if banker_value > 21 and player_value <= 21:
        player_wins += 1  # Banker busts, player wins
    elif player_value > banker_value:
        player_wins += 1  # Player wins
    elif player_value < banker_value:
        banker_wins += 1  # Banker wins
    else:
        ties += 1  # Tie situation

# Probability calculations
total_rounds = player_wins + banker_wins + ties + no_money_lost_or_gained
prob_player_win = player_wins / total_rounds * 100
prob_banker_win = banker_wins / total_rounds * 100
prob_tie = ties / total_rounds * 100
prob_no_money_lost_or_gained = no_money_lost_or_gained / total_rounds * 100

# Display results
prob_player_win, prob_banker_win, prob_tie, prob_no_money_lost_or_gained

print(f"Player wins: {player_wins} ({prob_player_win:.2f}%)")
print(f"Banker wins: {banker_wins} ({prob_banker_win:.2f}%)")
print(f"Ties: {ties} ({prob_tie:.2f}%)")
print(
    f"No money lost or gained: {no_money_lost_or_gained} ({prob_no_money_lost_or_gained:.2f}%)")
