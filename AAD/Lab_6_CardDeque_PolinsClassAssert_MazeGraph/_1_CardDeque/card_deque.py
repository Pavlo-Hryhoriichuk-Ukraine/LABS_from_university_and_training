from collections import deque


def play_cardgame(num_players: int, num_cards: int) -> tuple[int, set[int]]:
    cardboard: deque[int] = deque([0])
    scores: list[int] = [0] * num_players

    for card in range(1, num_cards):
        player_index = (card - 1) % num_players

        if card % 23 == 0:
            cardboard.rotate(7)
            score_7_card = cardboard.pop()

            scores[player_index] += card + score_7_card
        else:
            cardboard.rotate(-1)
            cardboard.append(card)

    winning_score = max(scores)
    winning_players = {
        i + 1 for i, score in enumerate(scores) if score == winning_score
    }

    return winning_score, winning_players


def test_play_cardgame() -> None:
    expected_score = 32
    expected_winners = {7}

    actual_score, actual_winners = play_cardgame(8, 25)
    print(actual_score)
    print(actual_winners)

    assert actual_score == expected_score, (
        f"Expected score {expected_score}, got {actual_score}"
    )
    assert actual_winners == expected_winners, (
        f"Expected winners {expected_winners}, got {actual_winners}"
    )


if __name__ == "__main__":
    test_play_cardgame()
