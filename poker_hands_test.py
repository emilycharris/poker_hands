from poker_hand import (find_multiples_of_a_kind, return_sorted_hand_by_value,
one_pair, two_pairs, three_of_a_kind, straight, flush, full_house,
four_of_a_kind, straight_flush, royal_flush, evaluate_hand, get_base_scores,
highest_card_tiebreaker, handle_tie, score_hands, read_and_parse_file,
calculate_winner)

# Test fixtures
pair_of_fives = ["5H", "5C", "6S", "7S", "KD"]
pair_of_eights = ["2C", "3S", "8S", "8D", "TD"]
pair_queens_highest_card_nine = ["4D", "6S", "9H", "QH", "QC"]
pair_queens_highest_card_seven = ["3D", "6D", "7H", "QD", "QS"]
two_pair_three_and_two = ["3C", "3H", "8S", "2D", "2C"]
three_aces = ["2D", "9C", "AS", "AH", "AC"]
four_threes = ["3D", "3C", "3S", "3H", "AC"]
straight_with_face_cards = ["TC", "JH", "QD", "KC", "AS"]
straight_flush_clubs = ["3C", "2C", "4C", "5C", "6C"]
highest_card_ace = ["5D", "8C", "9S", "JS", "AC"]
highest_card_queen = ["2C", "5C", "7D", "8S", "QH"]
flush_with_diamonds = ["3D", "6D", "7D", "TD", "QD"]
flush_with_face_cards = ["8H", "JH", "QH", "KH", "TH"]
full_house_with_three_fours = ["2H", "2D", "4C", "4D", "4S"]
full_house_with_three_threes = ["3C", "3D", "3S", "9S", "9D"]
royal_flush_hearts = ["TH", "JH", "QH", "KH", "AH"]

def test_find_multiples_of_a_kind():
    assert find_multiples_of_a_kind(pair_of_fives, 2) == ['5', '5']
    assert find_multiples_of_a_kind(three_aces, 3) == ['A', 'A', 'A']

def test_return_sorted_hand_by_value():
    assert return_sorted_hand_by_value(highest_card_ace) == [5, 8, 9, 11, 14]
    assert return_sorted_hand_by_value(highest_card_queen) == [2, 5, 7, 8, 12]

def test_one_pair():
    assert one_pair(pair_of_fives)['type'] == "One Pair"
    assert one_pair(highest_card_ace) == None

def test_two_pairs():
    assert two_pairs(two_pair_three_and_two)['type'] == "Two Pairs"
    assert two_pairs(pair_queens_highest_card_nine) == None

def test_three_of_a_kind():
    assert three_of_a_kind(three_aces)['type'] == "Three of a Kind"
    assert three_of_a_kind(pair_of_fives) == None

def test_straight():
    assert straight(straight_with_face_cards)['type'] == "Straight"
    assert straight(pair_queens_highest_card_seven) == None

def test_flush():
    assert flush(flush_with_diamonds)['type'] == "Flush"
    assert flush(three_aces) == None

def test_full_house():
    assert full_house(full_house_with_three_fours)['type'] == "Full House"
    assert full_house(full_house_with_three_threes)['type'] == "Full House"
    assert full_house(pair_of_eights) == None

def test_four_of_a_kind():
    assert four_of_a_kind(four_threes)['type'] == "Four of a Kind"
    assert four_of_a_kind(three_aces) == None

def test_straight_flush():
    assert straight_flush(straight_flush_clubs)['type'] == 'Straight Flush'
    assert straight_flush(flush_with_diamonds) == None

def test_royal_flush():
    assert royal_flush(royal_flush_hearts)['type'] == 'Royal Flush'
    assert royal_flush(straight_with_face_cards) == None
    assert royal_flush(flush_with_face_cards) == None

def test_evaluate_hand():
    pair_result = evaluate_hand(pair_of_eights)
    assert  pair_result['type'] == "One Pair"
    assert  pair_result['tiebreaker'] == 8

    two_pairs_result = evaluate_hand(two_pair_three_and_two)
    assert  two_pairs_result['type'] == "Two Pairs"
    assert  two_pairs_result['tiebreaker'] == 3

    three_of_a_kind_result = evaluate_hand(three_aces)
    assert three_of_a_kind_result['type'] == "Three of a Kind"
    assert three_of_a_kind_result['tiebreaker'] == 14

    straight_result = evaluate_hand(straight_with_face_cards)
    assert straight_result['type'] == "Straight"
    assert straight_result['high_cards'] == [10, 11, 12, 13, 14]

    flush_result = evaluate_hand(flush_with_face_cards)
    assert flush_result['type'] == "Flush"
    assert flush_result['high_cards'] == [8, 10, 11, 12, 13]

    full_house_result = evaluate_hand(full_house_with_three_fours)
    assert full_house_result['type'] == "Full House"
    assert full_house_result['tiebreaker'] == 4

    four_of_kind_result = evaluate_hand(four_threes)
    assert four_of_kind_result['type'] == "Four of a Kind"
    assert four_of_kind_result['tiebreaker'] == 3

    straight_flush_result = evaluate_hand(straight_flush_clubs)
    assert straight_flush_result['type'] == "Straight Flush"
    assert straight_flush_result['high_cards'] == [2, 3, 4, 5, 6]

    royal_flush_result = evaluate_hand(royal_flush_hearts)
    assert royal_flush_result['type'] == "Royal Flush"

def test_get_base_scores():
    assert get_base_scores("Highest Card") == (1)
    assert get_base_scores("One Pair") == (2)
    assert get_base_scores("Two Pairs") == (3)
    assert get_base_scores("Three of a Kind") == (4)
    assert get_base_scores("Straight") == (5)
    assert get_base_scores("Flush") == (6)
    assert get_base_scores("Full House") == (7)
    assert get_base_scores("Four of a Kind") == (8)
    assert get_base_scores("Straight Flush") == (9)
    assert get_base_scores("Royal Flush") == (10)

def test_highest_card_tiebreaker():
    player1_hand = [2, 6, 10, 11, 12]
    player2_hand = [2, 5, 9, 10, 12]
    assert highest_card_tiebreaker(player1_hand, player2_hand) == 1

def test_handle_tie():
    # tiebreaker determines winner
    player1_results = {'tiebreaker': 6, 'high_cards': [11], 'type': 'Two Pairs'}
    player2_results = {'tiebreaker': 7, 'high_cards': [11], 'type': 'Two Pairs'}
    assert handle_tie(player1_results, player2_results) == 2

    # highest value card determines winner if tiebreakers are the same
    player1_results = {'tiebreaker': 5, 'high_cards': [10, 11], 'type': 'Two Pairs'}
    player2_results = {'tiebreaker': 5, 'high_cards': [9, 11], 'type': 'Two Pairs'}
    assert handle_tie(player1_results, player2_results) == 1

def test_score_hands():
    assert score_hands(pair_of_fives + pair_of_eights) == 2
    assert score_hands(highest_card_ace + highest_card_queen) == 1
    assert score_hands(three_aces + flush_with_diamonds) == 2
    assert score_hands(pair_queens_highest_card_nine + pair_queens_highest_card_seven) == 1
    assert score_hands(full_house_with_three_fours + full_house_with_three_threes) == 1

def test_read_and_parse_file():
    assert read_and_parse_file()[0][0] == "8C"
    assert read_and_parse_file()[999][9] == "6C"

def test_calculate_winner():
    mock_line_array =[
        ['TD', '8C', '4H', '7C', 'TC', 'KC', '4C', '3H', '7S', 'KS'],
        ['JC', '6S', '5H', '2H', '2D', 'KD', '9D', '7C', 'AS', 'JS'],
        ['2H', '4S', '5C', '5S', 'TC', 'KC', 'JD', '6C', 'TS', '3C'],
        ['3D', 'KH', 'QD', '6C', '6S', 'AD', 'AS', '8H', '2H', 'QS'],
        ['2S', '8D', '8C', '4C', 'TS', '9S', '9D', '9C', 'AC', '3D']]
    assert calculate_winner(mock_line_array) == 2
