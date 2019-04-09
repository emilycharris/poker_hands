## Helpers for functions for determining hand type
def find_multiples_of_a_kind(hand, of_kind):
    card_values = [card[0] for card in hand]
    kinds = [value for value in card_values if card_values.count(value) == of_kind]
    if kinds:
        return kinds

def return_sorted_hand_by_value(hand):
    value_dict = {"2": 2,"3": 3,"4": 4,"5": 5,"6": 6,"7": 7,"8": 8,"9": 9,"T": 10,"J": 11,"Q": 12,"K": 13,"A": 14}
    card_values = [value_dict[card[0]] for card in hand]
    card_values.sort()
    return card_values

## Functions to determine hand type
def one_pair(hand):
    # Two cards of the same value
    pair_value = find_multiples_of_a_kind(hand, 2)
    if pair_value and len(set(pair_value)) == 1:
        others = [value for value in hand if not value.startswith(pair_value[0])]
        return {
            "tiebreaker": return_sorted_hand_by_value(pair_value)[0],
            "high_cards": return_sorted_hand_by_value(others),
            "type": "One Pair"
        }

def two_pairs(hand):
    # Two different pairs
    twos = find_multiples_of_a_kind(hand, 2)
    if twos and len(set(twos)) == 2:
        others = [value for value in hand if (not value.startswith(twos[0]) and not value.startswith(twos[-1]))]
        return {
            "tiebreaker": return_sorted_hand_by_value(twos)[-1],
            "high_cards": return_sorted_hand_by_value(others),
            "type": "Two Pairs"
        }

def three_of_a_kind(hand):
    # Three cards of the same value
    threes = find_multiples_of_a_kind(hand, 3)
    if threes:
        others = [value for value in hand if not value.startswith(threes[0])]
        return {
            "tiebreaker": return_sorted_hand_by_value(threes)[0],
            "high_cards": return_sorted_hand_by_value(others),
            "type": "Three of a Kind"
        }

def straight(hand):
    # All cards are consecutive values
    sort_order = [x for x in range(2, 15)]
    card_values = return_sorted_hand_by_value(hand)

    beginning_index = sort_order.index(card_values[0])
    ending_index = sort_order.index(card_values[0]) + 5
    expected_slice = sort_order[beginning_index:ending_index]

    if expected_slice == card_values:
        return {
            "high_cards": card_values,
            "type": "Straight"
        }

def flush(hand):
    # All cards of the same suit
    card_suits = [card[1] for card in hand]
    suits_are_the_same = all(x == card_suits[0] for x in card_suits)
    if suits_are_the_same:
        return {
            "high_cards": return_sorted_hand_by_value(hand),
            "type": "Flush"
        }

def full_house(hand):
    # Three of a kind and a pair
    threes = find_multiples_of_a_kind(hand, 3)
    twos = find_multiples_of_a_kind(hand, 2)
    if threes and twos:
        return {
            "tiebreaker": return_sorted_hand_by_value(threes)[0],
            "type": "Full House"
        }

def four_of_a_kind(hand):
    # Four cards of the same value.
    fours = find_multiples_of_a_kind(hand, 4)
    if fours:
        others = [value for value in hand if not value.startswith(fours[0])]
        return {
            "tiebreaker": return_sorted_hand_by_value(fours)[0],
            "high_cards": return_sorted_hand_by_value(others),
            "type": "Four of a Kind"
        }

def straight_flush(hand):
    # All cards are consecutive values of same suit
    card_suits = [card[1] for card in hand]
    suits_are_the_same = all(x == card_suits[0] for x in card_suits)
    if suits_are_the_same:
        if straight(hand):
            return {
                "high_cards": return_sorted_hand_by_value(hand),
                "type": "Straight Flush"
            }

def royal_flush(hand):
    #Ten, Jack, Queen, King, Ace, in same suit
    expected_values = ["T", "J", "Q", "K", "A"]
    card_values = [card[0] for card in hand]
    contains_all_values =  all(card in card_values for card in expected_values)
    card_suits = [card[1] for card in hand]
    suits_are_the_same = all(x == card_suits[0] for x in card_suits)
    if contains_all_values and suits_are_the_same:
        return {
            "type": "Royal Flush"
        }

## Functions for determining hand value
def evaluate_hand(hand):
    royal_flush_obj = royal_flush(hand)
    straight_flush_obj = straight_flush(hand)
    four_of_a_kind_obj = four_of_a_kind(hand)
    full_house_obj = full_house(hand)
    flush_obj = flush(hand)
    straight_obj = straight(hand)
    three_of_a_kind_obj = three_of_a_kind(hand)
    two_pairs_obj = two_pairs(hand)
    one_pair_obj = one_pair(hand)
    high_cards = return_sorted_hand_by_value(hand)

    if royal_flush_obj:
        return royal_flush_obj
    elif straight_flush_obj:
        return straight_flush_obj
    elif four_of_a_kind_obj:
        return four_of_a_kind_obj
    elif full_house_obj:
        return full_house_obj
    elif flush_obj:
        return flush_obj
    elif straight_obj:
        return straight_obj
    elif three_of_a_kind_obj:
        return three_of_a_kind_obj
    elif two_pairs_obj:
        return two_pairs_obj
    elif one_pair_obj:
        return one_pair_obj
    else:
        return {"high_cards": high_cards, "type": "Highest Card"}

def get_base_scores(type):
    # High card face values end at 14, so this starts at 15
    base = {
        "Highest Card": 1,
        "One Pair": 2,
        "Two Pairs": 3,
        "Three of a Kind": 4,
        "Straight": 5,
        "Flush": 6,
        "Full House": 7,
        "Four of a Kind": 8,
        "Straight Flush": 9,
        "Royal Flush": 10
    }
    return base[type]

def highest_card_tiebreaker(player1_cards, player2_cards):
    index = -1
    length_of_player1_array = len(player1_cards)
    length_of_player2_array = len(player2_cards)

    while index >= -length_of_player1_array:
        if player1_cards[index] > player2_cards[index]:
            return 1
            break
        elif player2_cards[index] > player1_cards[index]:
            return 2
            break
        else:
            index -= 1
    else:
        raise UserWarning("All cards are the same value!")

def handle_tie(player1_hand_results, player2_hand_results):
    try:
        player1_tiebreaker = player1_hand_results['tiebreaker']
        player2_tiebreaker = player2_hand_results['tiebreaker']
    except(KeyError):
        player1_tiebreaker = None
        player2_tiebreaker = None

    try:
        player1_cards = player1_hand_results["high_cards"]
        player2_cards = player2_hand_results["high_cards"]
    except(KeyError):
        player1_cards = []
        player2_cards = []

    if player1_tiebreaker and player2_tiebreaker:
        if player1_tiebreaker > player2_tiebreaker:
            return 1
        elif player2_tiebreaker > player1_tiebreaker:
            return 2
        else:
            winner = highest_card_tiebreaker(player1_cards, player2_cards)
            if winner != 1 and winner != 2:
                raise UserWarning("It's a tie and it shouldn't be!!!")
            else:
                return winner
    else:
        return highest_card_tiebreaker(player1_cards, player2_cards)

def score_hands(line):
    player1_hand = line[:5]
    player2_hand = line[5:]

    player1_hand_results = evaluate_hand(player1_hand)
    player2_hand_results = evaluate_hand(player2_hand)

    player1_score = get_base_scores(player1_hand_results["type"])
    player2_score = get_base_scores(player2_hand_results["type"])

    if player1_score == player2_score:
        winner = handle_tie(player1_hand_results, player2_hand_results)
        if winner == 1:
            return 1
        elif winner == 2:
            return 2
        else:
            print("There shouldn't be a tie here")
    elif player1_score > player2_score:
        return 1
    else:
        return 2

## Main functions
def read_and_parse_file():
    with open("poker.txt") as opened_file:
        file = opened_file.read()
        line_array = [line.upper().split(" ") for line in file.split("\n") if line != ""]
        return line_array

def calculate_winner(line_array):
    player1_total_wins = 0
    player2_total_wins = 0

    for line in line_array:
        winner = score_hands(line)

        if winner == 1:
            player1_total_wins += 1
        elif winner == 2:
            player2_total_wins += 1
        else:
            raise UserWarning("No defined winner! That can't happen!")

    print("Player1 won {} times".format(player1_total_wins))
    print("Player2 won {} times".format(player2_total_wins))
    return player1_total_wins


def main():
    file = read_and_parse_file()
    calculate_winner(file)

if __name__ == "__main__": main()
