# import random

# # Dictionary that converts each card label into its blackjack value.
# # Face cards all count as 10.
# # Ace starts as 11, but later we may reduce it to 1 if needed.
# CARD_VALUES = {
#     "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
#     "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11
# }

# # Set of valid card inputs the user is allowed to enter.
# VALID_CARDS = set(CARD_VALUES.keys())

# # Simplified deck for random drawing.
# # We are assuming a freshly shuffled deck every hand,
# # so we just choose random card values from this list.
# DECK = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


# def hand_value(hand):
#     """
#     Calculate the best blackjack value for a hand.

#     Aces are counted as 11 at first.
#     If the total goes over 21, we reduce one Ace from 11 to 1
#     by subtracting 10 from the total.
#     We keep doing that until the hand is 21 or less,
#     or until there are no more Aces left to adjust.
#     """
#     total = 0
#     aces = 0

#     # Add up the value of every card in the hand.
#     for card in hand:
#         total += CARD_VALUES[card]

#         # Count how many Aces are in the hand
#         # so we can adjust them later if needed.
#         if card == "A":
#             aces += 1

#     # If total is too high, convert Ace(s) from 11 to 1 as needed.
#     while total > 21 and aces > 0:
#         total -= 10
#         aces -= 1

#     return total


# def is_bust(hand):
#     """
#     Return True if the hand is over 21, otherwise False.
#     """
#     return hand_value(hand) > 21


# def draw_card():
#     """
#     Randomly choose one card from the simplified deck.
#     This supports the Monte Carlo simulation.
#     """
#     return random.choice(DECK)


# def simulate_dealer_hand(showing_card):
#     """
#     Simulate the dealer's play.

#     The dealer starts with:
#     - the visible showing card
#     - one random hidden card

#     Then the dealer keeps hitting until the total is 17 or more.
#     """
#     dealer_hand = [showing_card, draw_card()]

#     while hand_value(dealer_hand) < 17:
#         dealer_hand.append(draw_card())

#     return dealer_hand


# def compare_hands(player_hand, dealer_hand):
#     """
#     Compare the player's hand to the dealer's hand.

#     Return:
#     1  if the player wins
#     0  if it is a tie (push)
#     -1 if the player loses
#     """
#     player_total = hand_value(player_hand)
#     dealer_total = hand_value(dealer_hand)

#     # Player busts first = automatic loss.
#     if player_total > 21:
#         return -1

#     # Dealer busts = player wins.
#     if dealer_total > 21:
#         return 1

#     # Higher total wins.
#     if player_total > dealer_total:
#         return 1
#     if player_total < dealer_total:
#         return -1

#     # Equal totals = push.
#     return 0


# def simulate_stand(player_hand, dealer_showing, trials=5000):
#     """
#     Simulate what happens if the player stands right now.

#     We repeat the situation many times.
#     Each time:
#     - simulate the dealer's full hand
#     - compare the result

#     We return the average score across all trials.
#     A higher average score means better outcomes.
#     """
#     score = 0

#     for _ in range(trials):
#         dealer_hand = simulate_dealer_hand(dealer_showing)
#         score += compare_hands(player_hand, dealer_hand)

#     return score / trials


# def simulate_hit(player_hand, dealer_showing, trials=5000):
#     """
#     Simulate what happens if the player takes one hit right now.

#     Each trial:
#     - add one random card to the player's hand
#     - if player busts, count it as a loss
#     - otherwise simulate the dealer's hand and compare results

#     This keeps the project simple by testing one immediate hit
#     versus standing immediately.
#     """
#     score = 0

#     for _ in range(trials):
#         # Make a copy of the player's hand and add one random card.
#         new_hand = player_hand[:] + [draw_card()]

#         # If the player busts after the hit, count a loss.
#         if is_bust(new_hand):
#             score += -1
#         else:
#             # Otherwise simulate the dealer and compare outcomes.
#             dealer_hand = simulate_dealer_hand(dealer_showing)
#             score += compare_hands(new_hand, dealer_hand)

#     return score / trials


# def recommend_action(player_hand, dealer_showing, trials=5000):
#     """
#     Use Monte Carlo simulation to compare:
#     - standing now
#     - hitting now

#     Then return the recommendation and a short explanation.
#     """
#     stand_score = simulate_stand(player_hand, dealer_showing, trials)
#     hit_score = simulate_hit(player_hand, dealer_showing, trials)

#     if hit_score > stand_score:
#         recommendation = "Hit"
#         reason = (
#             f"In repeated simulations, hitting performed better than standing. "
#             f"(Hit score: {hit_score:.4f}, Stand score: {stand_score:.4f})"
#         )
#     else:
#         recommendation = "Stand"
#         reason = (
#             f"In repeated simulations, standing performed better than or equal to hitting. "
#             f"(Stand score: {stand_score:.4f}, Hit score: {hit_score:.4f})"
#         )

#     return recommendation, reason


# def get_valid_card(prompt_text):
#     """
#     Ask the user for a card until they enter a valid one.
#     Valid choices are 2-10, J, Q, K, or A.
#     """
#     while True:
#         card = input(prompt_text).strip().upper()
#         if card in VALID_CARDS:
#             return card
#         print("Invalid card. Please enter 2-10, J, Q, K, or A.")


# def get_player_hand():
#     """
#     Ask the user how many cards are currently in the player's hand,
#     then collect each card one at a time.
#     """
#     while True:
#         try:
#             num_cards = int(input("How many cards are in the player's hand? "))

#             # A blackjack hand should begin with at least two cards.
#             if num_cards < 2:
#                 print("A blackjack hand should start with at least 2 cards.")
#                 continue

#             hand = []

#             # Ask for each card separately.
#             for i in range(num_cards):
#                 card = get_valid_card(f"Enter Card {i + 1}: ")
#                 hand.append(card)

#             return hand

#         except ValueError:
#             print("Please enter a valid number.")


# def get_dealer_card():
#     """
#     Ask the user for the dealer's visible card.
#     """
#     return get_valid_card("Enter the dealer's showing card: ")


# def ask_to_add_card(player_hand):
#     """
#     Ask the user whether they want to add another card to the player's hand.

#     If yes:
#     - prompt for the next card
#     - append it to the hand
#     - return True

#     If no:
#     - return False
#     """
#     while True:
#         choice = input("Do you want to add a new card to the player's hand? (y/n): ").strip().lower()

#         if choice == "y":
#             new_card = get_valid_card(f"Enter Card {len(player_hand) + 1}: ")
#             player_hand.append(new_card)
#             return True
#         elif choice == "n":
#             return False
#         else:
#             print("Please enter y or n.")


# def ask_game_result():
#     """
#     If the user chooses not to add another card,
#     ask whether they won or lost the hand.
#     """
#     while True:
#         result = input("Did you win or lose this hand? (win/lose): ").strip().lower()

#         if result in ["win", "lose"]:
#             print(f"Recorded result: {result}")
#             return result

#         print("Please enter 'win' or 'lose'.")


# def ask_continue():
#     """
#     Ask the user if they want to start a new hand.
#     """
#     while True:
#         choice = input("Do you want to continue and start a new hand? (y/n): ").strip().lower()

#         if choice in ["y", "n"]:
#             return choice

#         print("Please enter y or n.")


# def play_hand():
#     """
#     Run one full blackjack advice cycle for a single hand.

#     Steps:
#     1. Get the player's starting hand
#     2. Get the dealer's showing card
#     3. Show the recommendation
#     4. Let the user add cards and re-evaluate as needed
#     5. If they stop adding cards, ask whether they won or lost
#     """
#     player_hand = get_player_hand()
#     dealer_showing = get_dealer_card()

#     while True:
#         print("\n" + "=" * 50)
#         print("Current player hand:", player_hand)
#         print("Current total:", hand_value(player_hand))
#         print("Dealer showing:", dealer_showing)

#         # If the player's hand is already over 21,
#         # the hand is over immediately.
#         if is_bust(player_hand):
#             print("The player is bust.")
#             break

#         # Use Monte Carlo simulation to generate the recommendation.
#         recommendation, reason = recommend_action(player_hand, dealer_showing)

#         print("\nRecommendation:", recommendation)
#         print("Reason:", reason)

#         # Ask whether the user wants to add another card and re-check.
#         added = ask_to_add_card(player_hand)

#         # If not, ask whether they won or lost and end this hand.
#         if not added:
#             ask_game_result()
#             break


# def main():
#     """
#     Main program loop.

#     This starts the app, plays one hand at a time,
#     and asks whether the user wants to continue.
#     """
#     print("=" * 60)
#     print("BLACKJACK HIT OR STAND ADVISOR")
#     print("Monte Carlo Simulation Console App")
#     print("=" * 60)

#     while True:
#         # Play one complete hand.
#         play_hand()

#         # Ask whether to start over with a new hand.
#         cont = ask_continue()

#         if cont == "n":
#             print("\nSession ended.")
#             break


# # This line makes sure main() runs only when this file
# # is executed directly, not when it is imported into another script.
# if __name__ == "__main__":
#     main()


# import random
# import time

# # -----------------------------
# # CONFIG
# # -----------------------------
# NUM_DECKS = 6
# RESHUFFLE_THRESHOLD = 52
# DEALER_HITS_SOFT_17 = False
# SLEEP_TIME = 0.5

# CARD_VALUES = {
#     "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
#     "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11
# }

# CARD_RANKS = list(CARD_VALUES.keys())
# SINGLE_DECK = CARD_RANKS * 4


# # -----------------------------
# # SHOE
# # -----------------------------
# class Shoe:
#     def __init__(self, num_decks=NUM_DECKS):
#         self.num_decks = num_decks
#         self.cards = []
#         self.shuffle()

#     def shuffle(self):
#         print("\n[Dealer is shuffling the shoe...]")
#         self.cards = SINGLE_DECK * self.num_decks
#         random.shuffle(self.cards)

#     def draw(self):
#         if len(self.cards) < RESHUFFLE_THRESHOLD:
#             self.shuffle()
#         return self.cards.pop()

#     def cards_remaining(self):
#         return len(self.cards)


# # -----------------------------
# # HAND
# # -----------------------------
# class Hand:
#     def __init__(self):
#         self.cards = []

#     def add_card(self, card):
#         self.cards.append(card)

#     def get_value(self):
#         total = sum(CARD_VALUES[c] for c in self.cards)
#         aces = self.cards.count("A")

#         while total > 21 and aces > 0:
#             total -= 10
#             aces -= 1

#         return total

#     def is_soft(self):
#         total = sum(CARD_VALUES[c] for c in self.cards)
#         aces = self.cards.count("A")
#         while total > 21 and aces > 0:
#             total -= 10
#             aces -= 1
#         return "A" in self.cards and total <= 21 and sum(CARD_VALUES[c] for c in self.cards) != total

#     def is_blackjack(self):
#         return len(self.cards) == 2 and self.get_value() == 21

#     def is_bust(self):
#         return self.get_value() > 21

#     def reset(self):
#         self.cards = []

#     def __str__(self):
#         soft_text = " soft" if self.is_soft() and self.get_value() <= 21 else ""
#         return f"{', '.join(self.cards)} (Total: {self.get_value()}{soft_text})"


# # -----------------------------
# # UTILITIES
# # -----------------------------
# def pause():
#     time.sleep(SLEEP_TIME)


# def get_int_input(prompt, min_val, max_val):
#     while True:
#         try:
#             value = int(input(prompt).strip())
#             if min_val <= value <= max_val:
#                 return value
#             print(f"Please enter a number between {min_val} and {max_val}.")
#         except ValueError:
#             print("Please enter a valid whole number.")


# def get_choice_input(prompt, valid_choices):
#     valid_choices = [c.lower() for c in valid_choices]
#     while True:
#         choice = input(prompt).strip().lower()
#         if choice in valid_choices:
#             return choice
#         print(f"Invalid input. Enter one of: {', '.join(valid_choices)}")


# # -----------------------------
# # BASIC STRATEGY LITE FOR NPCS
# # Not full casino strategy, just better than hit-until-17
# # -----------------------------
# def npc_should_hit(player_hand, dealer_upcard):
#     player_total = player_hand.get_value()
#     dealer_val = CARD_VALUES[dealer_upcard]
#     if dealer_upcard == "A":
#         dealer_val = 11

#     # Soft totals
#     if player_hand.is_soft():
#         if player_total <= 17:
#             return True
#         if player_total == 18:
#             return dealer_val in [9, 10, 11]
#         return False

#     # Hard totals
#     if player_total <= 11:
#         return True
#     if player_total == 12:
#         return dealer_val not in [4, 5, 6]
#     if 13 <= player_total <= 16:
#         return dealer_val >= 7
#     return False


# # -----------------------------
# # PLAYER TURNS
# # -----------------------------
# def play_npc_turn(name, hand, shoe, dealer_upcard):
#     print(f"\n--- {name}'s Turn ---")
#     print(f"{name}'s starting hand: {hand}")

#     if hand.is_blackjack():
#         print(f"{name} has BLACKJACK.")
#         return

#     while not hand.is_bust() and npc_should_hit(hand, dealer_upcard):
#         pause()
#         new_card = shoe.draw()
#         hand.add_card(new_card)
#         print(f"{name} hits and gets: {new_card}. New hand: {hand}")

#     if hand.is_bust():
#         print(f"{name} busts.")
#     else:
#         pause()
#         print(f"{name} stands with {hand.get_value()}.")


# def play_user_turn(name, hand, shoe):
#     print(f"\n--- YOUR TURN ({name}) ---")

#     if hand.is_blackjack():
#         print(f"Your hand: {hand}")
#         print("Blackjack!")
#         return

#     while True:
#         print(f"Your hand: {hand}")

#         if hand.is_bust():
#             print("You busted.")
#             return

#         if hand.get_value() == 21:
#             print("You have 21.")
#             return

#         choice = get_choice_input("Do you want to (H)it or (S)tand? ", ["h", "s"])

#         if choice == "h":
#             new_card = shoe.draw()
#             hand.add_card(new_card)
#             print(f"You drew a {new_card}.")
#         else:
#             print(f"You stand with {hand.get_value()}.")
#             return


# # -----------------------------
# # DEALER TURN
# # -----------------------------
# def dealer_should_hit(hand):
#     total = hand.get_value()
#     if total < 17:
#         return True
#     if total == 17 and DEALER_HITS_SOFT_17 and hand.is_soft():
#         return True
#     return False


# def play_dealer_turn(dealer_hand, shoe, any_live_players):
#     print("\n--- Dealer's Turn ---")
#     print(f"Dealer reveals hole card: {dealer_hand.cards[1]}. Hand: {dealer_hand}")

#     if dealer_hand.is_blackjack():
#         print("Dealer has BLACKJACK.")
#         return

#     if not any_live_players:
#         print("All players busted. Dealer wins by default.")
#         return

#     while dealer_should_hit(dealer_hand):
#         pause()
#         new_card = shoe.draw()
#         dealer_hand.add_card(new_card)
#         print(f"Dealer hits and gets: {new_card}. New hand: {dealer_hand}")

#     if dealer_hand.is_bust():
#         print("Dealer busts.")
#     else:
#         print(f"Dealer stands with {dealer_hand.get_value()}.")


# # -----------------------------
# # ROUND RESOLUTION
# # -----------------------------
# def resolve_hand(player_hand, dealer_hand):
#     if player_hand.is_blackjack() and dealer_hand.is_blackjack():
#         return "push_blackjack"
#     if player_hand.is_blackjack():
#         return "player_blackjack"
#     if dealer_hand.is_blackjack():
#         return "dealer_blackjack"
#     if player_hand.is_bust():
#         return "player_bust"
#     if dealer_hand.is_bust():
#         return "player_win"

#     p_total = player_hand.get_value()
#     d_total = dealer_hand.get_value()

#     if p_total > d_total:
#         return "player_win"
#     if p_total < d_total:
#         return "dealer_win"
#     return "push"


# def print_result(name, result, player_hand, dealer_hand):
#     p_total = player_hand.get_value()
#     d_total = dealer_hand.get_value()

#     if result == "push_blackjack":
#         print(f"{name} pushed. Both have blackjack.")
#     elif result == "player_blackjack":
#         print(f"{name} won with BLACKJACK.")
#     elif result == "dealer_blackjack":
#         print(f"{name} lost. Dealer has blackjack.")
#     elif result == "player_bust":
#         print(f"{name} busted and lost.")
#     elif result == "player_win":
#         print(f"{name} won ({p_total} vs {d_total}).")
#     elif result == "dealer_win":
#         print(f"{name} lost ({p_total} vs {d_total}).")
#     else:
#         print(f"{name} pushed (tied at {p_total}).")


# # -----------------------------
# # SETUP
# # -----------------------------
# def get_table_setup():
#     num_players = get_int_input("How many players are at the table? (1-5): ", 1, 5)
#     user_seat = get_int_input(f"Which seat are you in? (1-{num_players}, left to right): ", 1, num_players)
#     return num_players, user_seat


# # -----------------------------
# # ROUND
# # -----------------------------
# def play_round(shoe, num_players, user_seat, stats):
#     print("\n" + "=" * 50)
#     print("NEW ROUND STARTING")
#     print("=" * 50)
#     print(f"Cards remaining in shoe: {shoe.cards_remaining()}")

#     player_hands = {i: Hand() for i in range(1, num_players + 1)}
#     dealer_hand = Hand()

#     # Initial deal
#     for _ in range(2):
#         for i in range(1, num_players + 1):
#             player_hands[i].add_card(shoe.draw())
#         dealer_hand.add_card(shoe.draw())

#     dealer_upcard = dealer_hand.cards[0]
#     print(f"\nDealer shows: {dealer_upcard} and a [Hidden Card]")

#     for i in range(1, num_players + 1):
#         if i == user_seat:
#             print(f"Seat {i} (You): {player_hands[i]}")
#         else:
#             print(f"Seat {i} (NPC): {player_hands[i]}")

#     # Player turns
#     for i in range(1, num_players + 1):
#         if i == user_seat:
#             play_user_turn("Player", player_hands[i], shoe)
#         else:
#             play_npc_turn(f"NPC {i}", player_hands[i], shoe, dealer_upcard)

#     # Dealer turn
#     any_live_players = any(not h.is_bust() for h in player_hands.values())
#     play_dealer_turn(dealer_hand, shoe, any_live_players)

#     # Resolve results
#     print("\n--- RESULTS ---")
#     for i in range(1, num_players + 1):
#         hand = player_hands[i]
#         name = "You" if i == user_seat else f"NPC {i}"
#         result = resolve_hand(hand, dealer_hand)
#         print_result(name, result, hand, dealer_hand)

#         if i == user_seat:
#             stats["rounds"] += 1
#             if result in ["player_blackjack", "player_win"]:
#                 stats["wins"] += 1
#             elif result in ["dealer_blackjack", "player_bust", "dealer_win"]:
#                 stats["losses"] += 1
#             else:
#                 stats["pushes"] += 1

#     print("\n--- YOUR SESSION STATS ---")
#     print(f"Rounds: {stats['rounds']}")
#     print(f"Wins:   {stats['wins']}")
#     print(f"Losses: {stats['losses']}")
#     print(f"Pushes: {stats['pushes']}")


# # -----------------------------
# # MAIN
# # -----------------------------
# def main():
#     print("=" * 60)
#     print("CASINO BLACKJACK SIMULATOR")
#     print("=" * 60)

#     num_players, user_seat = get_table_setup()
#     shoe = Shoe(NUM_DECKS)

#     stats = {
#         "rounds": 0,
#         "wins": 0,
#         "losses": 0,
#         "pushes": 0
#     }

#     while True:
#         play_round(shoe, num_players, user_seat, stats)
#         choice = get_choice_input("\nDo you want to play another round? (y/n): ", ["y", "n"])
#         if choice != "y":
#             print("Leaving the table. Goodbye.")
#             break


# if __name__ == "__main__":
#     main()


# import random
# import time
# from collections import Counter

# # -----------------------------
# # CONFIG
# # -----------------------------
# NUM_DECKS = 6
# RESHUFFLE_THRESHOLD = 52
# DEALER_HITS_SOFT_17 = False
# SLEEP_TIME = 0.5
# MONTE_CARLO_TRIALS = 3000

# CARD_VALUES = {
#     "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
#     "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11
# }

# CARD_RANKS = list(CARD_VALUES.keys())
# SINGLE_DECK = CARD_RANKS * 4


# # -----------------------------
# # SHOE
# # -----------------------------
# class Shoe:
#     def __init__(self, num_decks=NUM_DECKS):
#         self.num_decks = num_decks
#         self.cards = []
#         self.shuffle()

#     def shuffle(self):
#         print("\n[Dealer is shuffling the shoe...]")
#         self.cards = SINGLE_DECK * self.num_decks
#         random.shuffle(self.cards)

#     def draw(self):
#         if len(self.cards) < RESHUFFLE_THRESHOLD:
#             self.shuffle()
#         return self.cards.pop()

#     def cards_remaining(self):
#         return len(self.cards)


# # -----------------------------
# # HAND
# # -----------------------------
# class Hand:
#     def __init__(self):
#         self.cards = []

#     def add_card(self, card):
#         self.cards.append(card)

#     def copy(self):
#         h = Hand()
#         h.cards = self.cards[:]
#         return h

#     def get_value(self):
#         total = sum(CARD_VALUES[c] for c in self.cards)
#         aces = self.cards.count("A")

#         while total > 21 and aces > 0:
#             total -= 10
#             aces -= 1

#         return total

#     def is_soft(self):
#         total = sum(CARD_VALUES[c] for c in self.cards)
#         aces = self.cards.count("A")
#         while total > 21 and aces > 0:
#             total -= 10
#             aces -= 1
#         return "A" in self.cards and total <= 21 and sum(CARD_VALUES[c] for c in self.cards) != total

#     def is_blackjack(self):
#         return len(self.cards) == 2 and self.get_value() == 21

#     def is_bust(self):
#         return self.get_value() > 21

#     def __str__(self):
#         soft_text = " soft" if self.is_soft() and self.get_value() <= 21 else ""
#         return f"{', '.join(self.cards)} (Total: {self.get_value()}{soft_text})"


# # -----------------------------
# # UTILITIES
# # -----------------------------
# def pause():
#     time.sleep(SLEEP_TIME)


# def get_int_input(prompt, min_val, max_val):
#     while True:
#         try:
#             value = int(input(prompt).strip())
#             if min_val <= value <= max_val:
#                 return value
#             print(f"Please enter a number between {min_val} and {max_val}.")
#         except ValueError:
#             print("Please enter a valid whole number.")


# def get_choice_input(prompt, valid_choices):
#     valid_choices = [c.lower() for c in valid_choices]
#     while True:
#         choice = input(prompt).strip().lower()
#         if choice in valid_choices:
#             return choice
#         print(f"Invalid input. Enter one of: {', '.join(valid_choices)}")


# # -----------------------------
# # NPC STRATEGY
# # -----------------------------
# def npc_should_hit(player_hand, dealer_upcard):
#     player_total = player_hand.get_value()
#     dealer_val = CARD_VALUES[dealer_upcard]
#     if dealer_upcard == "A":
#         dealer_val = 11

#     if player_hand.is_soft():
#         if player_total <= 17:
#             return True
#         if player_total == 18:
#             return dealer_val in [9, 10, 11]
#         return False

#     if player_total <= 11:
#         return True
#     if player_total == 12:
#         return dealer_val not in [4, 5, 6]
#     if 13 <= player_total <= 16:
#         return dealer_val >= 7
#     return False


# # -----------------------------
# # DEALER RULES
# # -----------------------------
# def dealer_should_hit(hand):
#     total = hand.get_value()
#     if total < 17:
#         return True
#     if total == 17 and DEALER_HITS_SOFT_17 and hand.is_soft():
#         return True
#     return False


# # -----------------------------
# # MONTE CARLO ADVISOR
# # -----------------------------
# def weighted_draw_from_cards(cards):
#     return random.choice(cards)


# def play_dealer_simulation(dealer_hand, remaining_cards):
#     dealer = dealer_hand.copy()
#     shoe_cards = remaining_cards[:]

#     while dealer_should_hit(dealer):
#         if not shoe_cards:
#             break
#         card = weighted_draw_from_cards(shoe_cards)
#         shoe_cards.remove(card)
#         dealer.add_card(card)

#     return dealer


# def compare_final_hands(player_hand, dealer_hand):
#     if player_hand.is_bust():
#         return -1
#     if dealer_hand.is_bust():
#         return 1

#     p = player_hand.get_value()
#     d = dealer_hand.get_value()

#     if p > d:
#         return 1
#     if p < d:
#         return -1
#     return 0


# def simulate_stand(player_hand, dealer_upcard, remaining_cards, trials=MONTE_CARLO_TRIALS):
#     wins = 0
#     pushes = 0
#     losses = 0

#     for _ in range(trials):
#         sim_cards = remaining_cards[:]

#         if not sim_cards:
#             continue

#         hole_card = weighted_draw_from_cards(sim_cards)
#         sim_cards.remove(hole_card)

#         dealer = Hand()
#         dealer.add_card(dealer_upcard)
#         dealer.add_card(hole_card)

#         final_dealer = play_dealer_simulation(dealer, sim_cards)
#         result = compare_final_hands(player_hand, final_dealer)

#         if result == 1:
#             wins += 1
#         elif result == 0:
#             pushes += 1
#         else:
#             losses += 1

#     return wins, pushes, losses


# def simulate_hit_once(player_hand, dealer_upcard, remaining_cards, trials=MONTE_CARLO_TRIALS):
#     wins = 0
#     pushes = 0
#     losses = 0

#     for _ in range(trials):
#         sim_cards = remaining_cards[:]

#         if not sim_cards:
#             continue

#         first_hit = weighted_draw_from_cards(sim_cards)
#         sim_cards.remove(first_hit)

#         new_player = player_hand.copy()
#         new_player.add_card(first_hit)

#         if new_player.is_bust():
#             losses += 1
#             continue

#         hole_card = weighted_draw_from_cards(sim_cards)
#         sim_cards.remove(hole_card)

#         dealer = Hand()
#         dealer.add_card(dealer_upcard)
#         dealer.add_card(hole_card)

#         # After one forced hit, player stands for comparison
#         final_dealer = play_dealer_simulation(dealer, sim_cards)
#         result = compare_final_hands(new_player, final_dealer)

#         if result == 1:
#             wins += 1
#         elif result == 0:
#             pushes += 1
#         else:
#             losses += 1

#     return wins, pushes, losses


# def pct(x, total):
#     return 0.0 if total == 0 else 100 * x / total


# def advisor_recommendation(player_hand, dealer_upcard, shoe_cards, trials=MONTE_CARLO_TRIALS):
#     stand_w, stand_p, stand_l = simulate_stand(player_hand, dealer_upcard, shoe_cards, trials)
#     hit_w, hit_p, hit_l = simulate_hit_once(player_hand, dealer_upcard, shoe_cards, trials)

#     stand_total = stand_w + stand_p + stand_l
#     hit_total = hit_w + hit_p + hit_l

#     stand_win_rate = pct(stand_w, stand_total)
#     hit_win_rate = pct(hit_w, hit_total)
#     stand_nonloss = pct(stand_w + stand_p, stand_total)
#     hit_nonloss = pct(hit_w + hit_p, hit_total)

#     if hit_win_rate > stand_win_rate:
#         rec = "HIT"
#         reason = "In repeated simulations, hitting produced a better win rate than standing."
#     else:
#         rec = "STAND"
#         reason = "In repeated simulations, standing produced a better win rate than hitting."

#     return {
#         "recommendation": rec,
#         "reason": reason,
#         "stand_win_rate": stand_win_rate,
#         "hit_win_rate": hit_win_rate,
#         "stand_nonloss_rate": stand_nonloss,
#         "hit_nonloss_rate": hit_nonloss,
#         "stand_record": (stand_w, stand_p, stand_l),
#         "hit_record": (hit_w, hit_p, hit_l),
#     }


# def show_advisor(player_hand, dealer_upcard, shoe_cards):
#     advice = advisor_recommendation(player_hand, dealer_upcard, shoe_cards)

#     print("\nMonte Carlo advisor:")
#     print(f"Stand win rate:     {advice['stand_win_rate']:.1f}%")
#     print(f"Hit win rate:       {advice['hit_win_rate']:.1f}%")
#     print(f"Stand non-loss rate:{advice['stand_nonloss_rate']:.1f}%")
#     print(f"Hit non-loss rate:  {advice['hit_nonloss_rate']:.1f}%")
#     print(f"Recommendation:     {advice['recommendation']}")
#     print(f"Reason: {advice['reason']}")


# # -----------------------------
# # PLAYER TURNS
# # -----------------------------
# def play_npc_turn(name, hand, shoe, dealer_upcard):
#     print(f"\n--- {name}'s Turn ---")
#     print(f"{name}'s starting hand: {hand}")

#     if hand.is_blackjack():
#         print(f"{name} has BLACKJACK.")
#         return

#     while not hand.is_bust() and npc_should_hit(hand, dealer_upcard):
#         pause()
#         new_card = shoe.draw()
#         hand.add_card(new_card)
#         print(f"{name} hits and gets: {new_card}. New hand: {hand}")

#     if hand.is_bust():
#         print(f"{name} busts.")
#     else:
#         pause()
#         print(f"{name} stands with {hand.get_value()}.")


# def play_user_turn(name, hand, shoe, dealer_upcard):
#     print(f"\n--- YOUR TURN ({name}) ---")

#     if hand.is_blackjack():
#         print(f"Your hand: {hand}")
#         print("Blackjack!")
#         return

#     while True:
#         print(f"Your hand: {hand}")

#         if hand.is_bust():
#             print("You busted.")
#             return

#         if hand.get_value() == 21:
#             print("You have 21.")
#             return

#         show_advisor(hand, dealer_upcard, shoe.cards[:])

#         choice = get_choice_input("Do you want to (H)it or (S)tand? ", ["h", "s"])

#         if choice == "h":
#             new_card = shoe.draw()
#             hand.add_card(new_card)
#             print(f"You drew a {new_card}.")
#         else:
#             print(f"You stand with {hand.get_value()}.")
#             return


# # -----------------------------
# # DEALER TURN
# # -----------------------------
# def play_dealer_turn(dealer_hand, shoe, any_live_players):
#     print("\n--- Dealer's Turn ---")
#     print(f"Dealer reveals hole card: {dealer_hand.cards[1]}. Hand: {dealer_hand}")

#     if dealer_hand.is_blackjack():
#         print("Dealer has BLACKJACK.")
#         return

#     if not any_live_players:
#         print("All players busted. Dealer wins by default.")
#         return

#     while dealer_should_hit(dealer_hand):
#         pause()
#         new_card = shoe.draw()
#         dealer_hand.add_card(new_card)
#         print(f"Dealer hits and gets: {new_card}. New hand: {dealer_hand}")

#     if dealer_hand.is_bust():
#         print("Dealer busts.")
#     else:
#         print(f"Dealer stands with {dealer_hand.get_value()}.")


# # -----------------------------
# # RESULTS
# # -----------------------------
# def resolve_hand(player_hand, dealer_hand):
#     if player_hand.is_blackjack() and dealer_hand.is_blackjack():
#         return "push_blackjack"
#     if player_hand.is_blackjack():
#         return "player_blackjack"
#     if dealer_hand.is_blackjack():
#         return "dealer_blackjack"
#     if player_hand.is_bust():
#         return "player_bust"
#     if dealer_hand.is_bust():
#         return "player_win"

#     p_total = player_hand.get_value()
#     d_total = dealer_hand.get_value()

#     if p_total > d_total:
#         return "player_win"
#     if p_total < d_total:
#         return "dealer_win"
#     return "push"


# def print_result(name, result, player_hand, dealer_hand):
#     p_total = player_hand.get_value()
#     d_total = dealer_hand.get_value()

#     if result == "push_blackjack":
#         print(f"{name} pushed. Both have blackjack.")
#     elif result == "player_blackjack":
#         print(f"{name} won with BLACKJACK.")
#     elif result == "dealer_blackjack":
#         print(f"{name} lost. Dealer has blackjack.")
#     elif result == "player_bust":
#         print(f"{name} busted and lost.")
#     elif result == "player_win":
#         print(f"{name} won ({p_total} vs {d_total}).")
#     elif result == "dealer_win":
#         print(f"{name} lost ({p_total} vs {d_total}).")
#     else:
#         print(f"{name} pushed (tied at {p_total}).")


# # -----------------------------
# # SETUP
# # -----------------------------
# def get_table_setup():
#     num_players = get_int_input("How many players are at the table? (1-5): ", 1, 5)
#     user_seat = get_int_input(f"Which seat are you in? (1-{num_players}, left to right): ", 1, num_players)
#     return num_players, user_seat


# # -----------------------------
# # ROUND
# # -----------------------------
# def play_round(shoe, num_players, user_seat, stats):
#     print("\n" + "=" * 50)
#     print("NEW ROUND STARTING")
#     print("=" * 50)
#     print(f"Cards remaining in shoe: {shoe.cards_remaining()}")

#     player_hands = {i: Hand() for i in range(1, num_players + 1)}
#     dealer_hand = Hand()

#     for _ in range(2):
#         for i in range(1, num_players + 1):
#             player_hands[i].add_card(shoe.draw())
#         dealer_hand.add_card(shoe.draw())

#     dealer_upcard = dealer_hand.cards[0]
#     print(f"\nDealer shows: {dealer_upcard} and a [Hidden Card]")

#     for i in range(1, num_players + 1):
#         if i == user_seat:
#             print(f"Seat {i} (You): {player_hands[i]}")
#         else:
#             print(f"Seat {i} (NPC): {player_hands[i]}")

#     for i in range(1, num_players + 1):
#         if i == user_seat:
#             play_user_turn("Player", player_hands[i], shoe, dealer_upcard)
#         else:
#             play_npc_turn(f"NPC {i}", player_hands[i], shoe, dealer_upcard)

#     any_live_players = any(not h.is_bust() for h in player_hands.values())
#     play_dealer_turn(dealer_hand, shoe, any_live_players)

#     print("\n--- RESULTS ---")
#     for i in range(1, num_players + 1):
#         hand = player_hands[i]
#         name = "You" if i == user_seat else f"NPC {i}"
#         result = resolve_hand(hand, dealer_hand)
#         print_result(name, result, hand, dealer_hand)

#         if i == user_seat:
#             stats["rounds"] += 1
#             if result in ["player_blackjack", "player_win"]:
#                 stats["wins"] += 1
#             elif result in ["dealer_blackjack", "player_bust", "dealer_win"]:
#                 stats["losses"] += 1
#             else:
#                 stats["pushes"] += 1

#     print("\n--- YOUR SESSION STATS ---")
#     print(f"Rounds: {stats['rounds']}")
#     print(f"Wins:   {stats['wins']}")
#     print(f"Losses: {stats['losses']}")
#     print(f"Pushes: {stats['pushes']}")


# # -----------------------------
# # MAIN
# # -----------------------------
# def main():
#     print("=" * 60)
#     print("CASINO BLACKJACK SIMULATOR WITH ADVISOR")
#     print("=" * 60)

#     num_players, user_seat = get_table_setup()
#     shoe = Shoe(NUM_DECKS)

#     stats = {
#         "rounds": 0,
#         "wins": 0,
#         "losses": 0,
#         "pushes": 0
#     }

#     while True:
#         play_round(shoe, num_players, user_seat, stats)
#         choice = get_choice_input("\nDo you want to play another round? (y/n): ", ["y", "n"])
#         if choice != "y":
#             print("Leaving the table. Goodbye.")
#             break


# if __name__ == "__main__":
#     main()

import random

# ============================================================
# CASINO BLACKJACK SIMULATOR WITH MONTE CARLO ADVISOR
# ============================================================
#
# This program simulates a blackjack table with:
# - one human player
# - multiple NPC players
# - a dealer
# - a 6-deck shoe
#
# It also includes a Monte Carlo advisor for the human player.
# The advisor compares two choices from the current position:
#   1. Stand now
#   2. Hit now
#
# The advisor runs many random simulations from the CURRENT
# remaining shoe state, then compares the results using:
# - win rate
# - non-loss rate (win + push)
# - expected value (win = +1, push = 0, loss = -1)
#
# Important:
# Monte Carlo does not predict the next exact card.
# It estimates which decision performs better over many trials.
# ============================================================


# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------

NUM_DECKS = 6
SIMULATION_TRIALS = 5000

# If True, dealer stands on soft 17.
# If False, dealer hits soft 17.
DEALER_STANDS_SOFT_17 = True

# Simplified NPC strategy:
# NPC hits until at least this total.
NPC_HIT_THRESHOLD = 17


# ------------------------------------------------------------
# CARD / HAND UTILITIES
# ------------------------------------------------------------

# Rank values used for blackjack scoring.
CARD_VALUES = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11
}

VALID_CARDS = set(CARD_VALUES.keys())

# One standard deck by rank only.
# We do not track suits because suits do not matter in blackjack.
SINGLE_DECK_RANKS = [
    "2", "3", "4", "5", "6", "7", "8", "9", "10",
    "J", "Q", "K", "A"
]

# Four of each rank per physical deck.
SINGLE_DECK_SHOE = []
for rank in SINGLE_DECK_RANKS:
    SINGLE_DECK_SHOE.extend([rank] * 4)


def build_shoe(num_decks=NUM_DECKS):
    """
    Build a blackjack shoe with the requested number of decks,
    then shuffle it.
    """
    shoe = SINGLE_DECK_SHOE * num_decks
    random.shuffle(shoe)
    return shoe


def draw_from_shoe(shoe):
    """
    Remove and return one card from the shoe.
    We pop from the end for efficiency.
    """
    if not shoe:
        raise ValueError("The shoe is empty.")
    return shoe.pop()


def hand_value(hand):
    """
    Compute the best blackjack total for a hand.

    Aces are initially counted as 11.
    If the hand busts, we reduce one Ace at a time from 11 to 1
    by subtracting 10 from the total until the hand no longer busts
    or there are no more Aces left to adjust.
    """
    total = 0
    aces = 0

    for card in hand:
        total += CARD_VALUES[card]
        if card == "A":
            aces += 1

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total


def is_soft_hand(hand):
    """
    Return True if the hand is 'soft', meaning at least one Ace
    is still effectively being counted as 11 in the final total.
    """
    total = 0
    aces = 0

    for card in hand:
        total += CARD_VALUES[card]
        if card == "A":
            aces += 1

    # Reduce Aces only as needed.
    adjusted_aces = aces
    while total > 21 and adjusted_aces > 0:
        total -= 10
        adjusted_aces -= 1

    # If at least one Ace remains unadjusted, hand is soft.
    return aces > adjusted_aces


def is_blackjack(hand):
    """
    A natural blackjack is exactly two cards totaling 21.
    """
    return len(hand) == 2 and hand_value(hand) == 21


def is_bust(hand):
    """
    Return True if the hand total exceeds 21.
    """
    return hand_value(hand) > 21


def format_hand(hand):
    """
    Convert a list of cards into a comma-separated display string.
    """
    return ", ".join(hand)


def result_label(result):
    """
    Convert numerical result to text.
    1  = win
    0  = push
    -1 = loss
    """
    if result == 1:
        return "win"
    if result == 0:
        return "push"
    return "loss"


# ------------------------------------------------------------
# INPUT HELPERS
# ------------------------------------------------------------

def get_int_input(prompt, min_value=None, max_value=None):
    """
    Ask for an integer until the user enters a valid one.
    Optionally enforce a minimum and maximum.
    """
    while True:
        try:
            value = int(input(prompt).strip())
            if min_value is not None and value < min_value:
                print(f"Please enter a value >= {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"Please enter a value <= {max_value}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def get_h_or_s():
    """
    Ask the player whether to Hit or Stand.
    """
    while True:
        choice = input("Do you want to (H)it or (S)tand? ").strip().upper()
        if choice in ["H", "S"]:
            return choice
        print("Please enter H or S.")


def ask_play_again():
    """
    Ask the user whether to play another round.
    """
    while True:
        choice = input("Do you want to play another round? (y/n): ").strip().lower()
        if choice in ["y", "n"]:
            return choice
        print("Please enter y or n.")


# ------------------------------------------------------------
# SHOE MANIPULATION FOR MONTE CARLO
# ------------------------------------------------------------

def remove_known_cards_from_shoe(shoe, cards):
    """
    Remove a list of known cards from a COPY of the shoe.

    This is important for Monte Carlo simulation.
    We do not want to simulate from a fresh infinite deck if the
    visible game is using a finite shoe with known cards already dealt.
    """
    shoe_copy = shoe[:]
    for card in cards:
        try:
            shoe_copy.remove(card)
        except ValueError:
            # If a card is not found, something is inconsistent.
            # We raise a clear error rather than silently ignore it.
            raise ValueError(f"Could not remove known card {card} from simulation shoe.")
    return shoe_copy


# ------------------------------------------------------------
# DEALER LOGIC
# ------------------------------------------------------------

def dealer_should_hit(hand):
    """
    Determine whether the dealer should hit based on house rules.
    """
    total = hand_value(hand)

    # Dealer always hits below 17.
    if total < 17:
        return True

    # Dealer behavior on soft 17 depends on configuration.
    if total == 17 and is_soft_hand(hand):
        return not DEALER_STANDS_SOFT_17

    return False


def play_out_dealer_hand(dealer_hand, shoe):
    """
    Play the dealer's hand to completion using house rules.
    """
    while dealer_should_hit(dealer_hand):
        dealer_hand.append(draw_from_shoe(shoe))
    return dealer_hand


# ------------------------------------------------------------
# HAND COMPARISON
# ------------------------------------------------------------

def compare_player_vs_dealer(player_hand, dealer_hand):
    """
    Compare a finished player hand and dealer hand.

    Returns:
    1  if player wins
    0  if push
    -1 if player loses

    This version includes natural blackjack handling.
    """
    player_total = hand_value(player_hand)
    dealer_total = hand_value(dealer_hand)

    player_bj = is_blackjack(player_hand)
    dealer_bj = is_blackjack(dealer_hand)

    # Natural blackjack logic first.
    if player_bj and dealer_bj:
        return 0
    if player_bj:
        return 1
    if dealer_bj:
        return -1

    # Bust logic.
    if player_total > 21:
        return -1
    if dealer_total > 21:
        return 1

    # Standard comparison.
    if player_total > dealer_total:
        return 1
    if player_total < dealer_total:
        return -1
    return 0


# ------------------------------------------------------------
# NPC STRATEGY
# ------------------------------------------------------------

def npc_should_hit(hand):
    """
    Very simple NPC policy:
    hit until reaching at least NPC_HIT_THRESHOLD.
    """
    return hand_value(hand) < NPC_HIT_THRESHOLD


def play_npc_hand(hand, shoe, seat_number):
    """
    Play one NPC hand in the live round.
    """
    print(f"\n--- NPC {seat_number}'s Turn ---")
    print(f"NPC {seat_number}'s starting hand: {format_hand(hand)} (Total: {hand_value(hand)})")

    while npc_should_hit(hand):
        new_card = draw_from_shoe(shoe)
        hand.append(new_card)
        print(f"NPC {seat_number} hits and gets: {new_card}. New hand: {format_hand(hand)} (Total: {hand_value(hand)})")
        if is_bust(hand):
            print(f"NPC {seat_number} busts.")
            return hand

    print(f"NPC {seat_number} stands with {hand_value(hand)}.")
    return hand


# ------------------------------------------------------------
# MONTE CARLO ADVISOR
# ------------------------------------------------------------

def simulate_stand_once(player_hand, dealer_upcard, dealer_hole_unknown_shoe):
    """
    Simulate one trial where the player stands immediately.

    Steps:
    1. Draw a random dealer hole card from the remaining shoe.
    2. Play out the dealer hand.
    3. Compare player vs dealer.

    Returns:
    1  = player win
    0  = push
    -1 = loss
    """
    sim_shoe = dealer_hole_unknown_shoe[:]
    random.shuffle(sim_shoe)

    dealer_hand = [dealer_upcard, draw_from_shoe(sim_shoe)]
    play_out_dealer_hand(dealer_hand, sim_shoe)

    return compare_player_vs_dealer(player_hand, dealer_hand)


def simulate_hit_once(player_hand, dealer_upcard, dealer_hole_unknown_shoe):
    """
    Simulate one trial where the player takes one hit now.

    This version uses a simple continuation policy:
    after the first hit, the simulated player continues hitting
    until reaching 17 or more.

    That is more realistic than 'one hit then always stand', while
    still keeping the simulation understandable for classroom use.
    """
    sim_shoe = dealer_hole_unknown_shoe[:]
    random.shuffle(sim_shoe)

    sim_player = player_hand[:]
    sim_player.append(draw_from_shoe(sim_shoe))

    if is_bust(sim_player):
        return -1

    # Continue the simulated hand with a simple policy.
    while hand_value(sim_player) < 17:
        sim_player.append(draw_from_shoe(sim_shoe))
        if is_bust(sim_player):
            return -1

    dealer_hand = [dealer_upcard, draw_from_shoe(sim_shoe)]
    play_out_dealer_hand(dealer_hand, sim_shoe)

    return compare_player_vs_dealer(sim_player, dealer_hand)


def monte_carlo_advice(player_hand, dealer_upcard, known_cards, full_shoe, trials=SIMULATION_TRIALS):
    """
    Run Monte Carlo simulation from the current game state.

    known_cards should include all cards already visible/known in the
    current round that must be removed from the simulation shoe.

    full_shoe is the current real shoe state before simulation.

    We compare:
    - standing now
    - hitting now

    Recommendation is based primarily on expected value (EV):
      win  = +1
      push =  0
      loss = -1
    """
    # Build a simulation shoe that removes all known dealt cards.
    simulation_base_shoe = remove_known_cards_from_shoe(full_shoe, known_cards)

    stand_wins = 0
    stand_pushes = 0
    stand_losses = 0

    hit_wins = 0
    hit_pushes = 0
    hit_losses = 0

    for _ in range(trials):
        stand_result = simulate_stand_once(player_hand, dealer_upcard, simulation_base_shoe)
        hit_result = simulate_hit_once(player_hand, dealer_upcard, simulation_base_shoe)

        if stand_result == 1:
            stand_wins += 1
        elif stand_result == 0:
            stand_pushes += 1
        else:
            stand_losses += 1

        if hit_result == 1:
            hit_wins += 1
        elif hit_result == 0:
            hit_pushes += 1
        else:
            hit_losses += 1

    # Win rate = wins / trials
    stand_win_rate = stand_wins / trials
    hit_win_rate = hit_wins / trials

    # Non-loss rate = (wins + pushes) / trials
    stand_non_loss_rate = (stand_wins + stand_pushes) / trials
    hit_non_loss_rate = (hit_wins + hit_pushes) / trials

    # Expected value = (wins - losses) / trials
    # Since push contributes 0.
    stand_ev = (stand_wins - stand_losses) / trials
    hit_ev = (hit_wins - hit_losses) / trials

    # Recommendation uses EV first.
    if hit_ev > stand_ev:
        recommendation = "HIT"
        reason = "In repeated simulations from the current shoe state, hitting had the higher expected value."
    else:
        recommendation = "STAND"
        reason = "In repeated simulations from the current shoe state, standing had the higher expected value."

    return {
        "stand_win_rate": stand_win_rate,
        "hit_win_rate": hit_win_rate,
        "stand_non_loss_rate": stand_non_loss_rate,
        "hit_non_loss_rate": hit_non_loss_rate,
        "stand_ev": stand_ev,
        "hit_ev": hit_ev,
        "recommendation": recommendation,
        "reason": reason
    }


# ------------------------------------------------------------
# ROUND SETUP
# ------------------------------------------------------------

def deal_initial_round(shoe, num_players):
    """
    Deal the initial cards for one round.

    Returns:
    - dealer_hand
    - players_hands

    Each player gets two cards.
    Dealer gets two cards, one shown and one hidden.
    """
    players_hands = [[] for _ in range(num_players)]
    dealer_hand = []

    # First card to each player.
    for i in range(num_players):
        players_hands[i].append(draw_from_shoe(shoe))

    # Dealer first card (upcard).
    dealer_hand.append(draw_from_shoe(shoe))

    # Second card to each player.
    for i in range(num_players):
        players_hands[i].append(draw_from_shoe(shoe))

    # Dealer hole card.
    dealer_hand.append(draw_from_shoe(shoe))

    return dealer_hand, players_hands


def collect_known_cards_for_advisor(dealer_hand, players_hands):
    """
    Collect all cards currently known to the table for simulation.

    For fairness, the advisor should know:
    - all player cards
    - dealer upcard

    It should NOT know the dealer hole card.

    Since the live table has already dealt all player cards, it is
    reasonable to include all player initial cards, including NPC cards,
    because those cards really are out of the shoe.
    """
    known = []

    # Dealer upcard only, not the hidden hole card.
    known.append(dealer_hand[0])

    # All player cards currently dealt are out of the shoe.
    for hand in players_hands:
        known.extend(hand)

    return known


def print_table_state(dealer_hand, players_hands, user_seat):
    """
    Print the visible table at the beginning of the round.
    """
    print("\n" + "=" * 50)
    print("NEW ROUND STARTING")
    print("=" * 50)

    print(f"\nDealer shows: {dealer_hand[0]} and a [Hidden Card]")

    for i, hand in enumerate(players_hands, start=1):
        label = "You" if i == user_seat else "NPC"
        print(f"Seat {i} ({label}): {format_hand(hand)} (Total: {hand_value(hand)})")


# ------------------------------------------------------------
# LIVE PLAYER TURN
# ------------------------------------------------------------

def play_user_turn(user_hand, dealer_hand, players_hands, shoe, user_seat):
    """
    Handle the human player's turn.

    Before each decision, show a Monte Carlo recommendation based on:
    - the user's current hand
    - dealer upcard
    - the current remaining shoe
    - all known dealt cards
    """
    print("\n--- YOUR TURN (Player) ---")

    while True:
        print(f"Your hand: {format_hand(user_hand)} (Total: {hand_value(user_hand)})")

        if is_bust(user_hand):
            print("You busted.")
            return user_hand

        known_cards = collect_known_cards_for_advisor(dealer_hand, players_hands)

        advice = monte_carlo_advice(
            player_hand=user_hand,
            dealer_upcard=dealer_hand[0],
            known_cards=known_cards,
            full_shoe=shoe,
            trials=SIMULATION_TRIALS
        )

        print("\nMonte Carlo advisor:")
        print(f"Stand win rate:      {advice['stand_win_rate'] * 100:.1f}%")
        print(f"Hit win rate:        {advice['hit_win_rate'] * 100:.1f}%")
        print(f"Stand non-loss rate: {advice['stand_non_loss_rate'] * 100:.1f}%")
        print(f"Hit non-loss rate:   {advice['hit_non_loss_rate'] * 100:.1f}%")
        print(f"Stand EV:            {advice['stand_ev']:.3f}")
        print(f"Hit EV:              {advice['hit_ev']:.3f}")
        print(f"Recommendation:      {advice['recommendation']}")
        print(f"Reason: {advice['reason']}")

        choice = get_h_or_s()

        if choice == "S":
            print(f"You stand with {hand_value(user_hand)}.")
            return user_hand

        new_card = draw_from_shoe(shoe)
        user_hand.append(new_card)
        print(f"You drew a {new_card}.")


# ------------------------------------------------------------
# DEALER LIVE TURN
# ------------------------------------------------------------

def play_dealer_live_turn(dealer_hand, shoe):
    """
    Reveal the dealer hole card and then play the dealer hand
    according to the configured house rules.
    """
    print("\n--- Dealer's Turn ---")
    soft_text = " soft" if is_soft_hand(dealer_hand) and hand_value(dealer_hand) == 17 else ""
    print(f"Dealer reveals hole card: {dealer_hand[1]}. Hand: {format_hand(dealer_hand)} (Total: {hand_value(dealer_hand)}{soft_text})")

    while dealer_should_hit(dealer_hand):
        new_card = draw_from_shoe(shoe)
        dealer_hand.append(new_card)
        soft_text = " soft" if is_soft_hand(dealer_hand) and hand_value(dealer_hand) == 17 else ""
        print(f"Dealer hits and gets: {new_card}. New hand: {format_hand(dealer_hand)} (Total: {hand_value(dealer_hand)}{soft_text})")

    print(f"Dealer stands with {hand_value(dealer_hand)}.")
    return dealer_hand


# ------------------------------------------------------------
# ROUND RESOLUTION
# ------------------------------------------------------------

def summarize_round(dealer_hand, players_hands, user_seat):
    """
    Compare each player against the dealer and print results.

    Returns the result for the human player:
    1  = win
    0  = push
    -1 = loss
    """
    print("\n--- RESULTS ---")

    dealer_total = hand_value(dealer_hand)
    user_result = None

    for i, hand in enumerate(players_hands, start=1):
        result = compare_player_vs_dealer(hand, dealer_hand)
        total = hand_value(hand)

        if is_bust(hand):
            message = "busted and lost"
        elif result == 1:
            message = f"won ({total} vs {dealer_total})"
        elif result == 0:
            message = f"pushed ({total} vs {dealer_total})"
        else:
            message = f"lost ({total} vs {dealer_total})"

        if i == user_seat:
            print(f"You {message}.")
            user_result = result
        else:
            print(f"NPC {i} {message}.")

    return user_result


# ------------------------------------------------------------
# SESSION STATS
# ------------------------------------------------------------

def print_session_stats(stats):
    """
    Print cumulative results for the human player.
    """
    print("\n--- YOUR SESSION STATS ---")
    print(f"Rounds: {stats['rounds']}")
    print(f"Wins:   {stats['wins']}")
    print(f"Losses: {stats['losses']}")
    print(f"Pushes: {stats['pushes']}")


def update_session_stats(stats, result):
    """
    Update cumulative session counts after one round.
    """
    stats["rounds"] += 1
    if result == 1:
        stats["wins"] += 1
    elif result == 0:
        stats["pushes"] += 1
    else:
        stats["losses"] += 1


# ------------------------------------------------------------
# MAIN GAME LOOP
# ------------------------------------------------------------

def play_round(shoe, num_players, user_seat, stats):
    """
    Play one full round of blackjack.
    """
    # If the shoe gets low, rebuild and shuffle.
    # This keeps the game running cleanly.
    if len(shoe) < 52:
        print("\n[Dealer is shuffling the shoe...]")
        shoe[:] = build_shoe(NUM_DECKS)

    print(f"\nCards remaining in shoe: {len(shoe)}")

    dealer_hand, players_hands = deal_initial_round(shoe, num_players)
    print_table_state(dealer_hand, players_hands, user_seat)

    # Human player turn.
    user_hand = players_hands[user_seat - 1]
    play_user_turn(user_hand, dealer_hand, players_hands, shoe, user_seat)

    # NPC turns.
    for seat in range(1, num_players + 1):
        if seat == user_seat:
            continue
        npc_hand = players_hands[seat - 1]
        play_npc_hand(npc_hand, shoe, seat)

    # Dealer turn.
    play_dealer_live_turn(dealer_hand, shoe)

    # Round results.
    user_result = summarize_round(dealer_hand, players_hands, user_seat)
    update_session_stats(stats, user_result)
    print_session_stats(stats)


def main():
    """
    Start the blackjack table session and keep running rounds
    until the user chooses to stop.
    """
    print("=" * 60)
    print("CASINO BLACKJACK SIMULATOR WITH ADVISOR")
    print("=" * 60)

    num_players = get_int_input("How many players are at the table? (1-5): ", 1, 5)
    user_seat = get_int_input(f"Which seat are you in? (1-{num_players}, left to right): ", 1, num_players)

    shoe = build_shoe(NUM_DECKS)

    print("\n[Dealer is shuffling the shoe...]")

    stats = {
        "rounds": 0,
        "wins": 0,
        "losses": 0,
        "pushes": 0
    }

    while True:
        play_round(shoe, num_players, user_seat, stats)
        again = ask_play_again()

        if again == "n":
            print("Leaving the table. Goodbye.")
            break


# Run the program only when this file is executed directly.
if __name__ == "__main__":
    main()