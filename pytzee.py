import random

TOTAL_DICE = 5
DICE_FACES = 6
COUNT_TYPES = [
    "three of a kind",
    "four of a kind",
    "full house",
    "small straight",
    "large straight",
    "pytzee",
    "chance",
]
SCORES = [[0 for _ in range(DICE_FACES)], [0 for _ in range(len(COUNT_TYPES))]]

def roll_dice():
    """
    :return: a list containing five integers representing dice rolls between 1 and 6.
    """

    return [random.randint(1, 6) for _ in range(TOTAL_DICE)]

def get_score(scores):
    score = 0

    for lists in scores:
        for i in lists:
            score += i

    return score

def display_scorecard():
    card = f"Scorecard:\n"

    for scores in SCORES:
        if len(scores) == 6:
            for i in range(6):
                card += f"{i+1}'s\t\t"

            card += '\n'

            for i in scores:
                card += f"{i}\t\t"
        else:
            for i in range(len(scores)):
                title = COUNT_TYPES[i]
                card += f"{title}\n{scores[i]}\n"

        card += '\n'

    print(card)

def find_patterns(dice_rolls, pattern_to_find):
    points = 0

    if pattern_to_find == "pytzee":
        side = dice_rolls[0]

        for i in dice_rolls:
            if i != side:
                return 0

        points = 50
    else:

        if pattern_to_find == "three of a kind" or pattern_to_find == "3 of a kind"\
                or pattern_to_find == "four of a kind" or pattern_to_find == "4 of a kind"\
                or pattern_to_find == "full house":
            rolls = ['' for _ in range(DICE_FACES)]
            patterns_found = []

            for i in range(TOTAL_DICE):
                rolls[dice_rolls[i] - 1] += str(dice_rolls[i])

            for i in rolls:
                if ((pattern_to_find == "full house" or "three" in pattern_to_find or "3" in pattern_to_find) and len(i) >= 3)\
                        or (('four' in pattern_to_find or "4" in pattern_to_find) and len(i) >= 4):
                    # (number, occurrence)
                    patterns_found.append((int(i[0]), len(i)))

            #print(rolls, dice_rolls, patterns_found)

            if patterns_found:
                if pattern_to_find == "full house":
                    for str_num in rolls:
                        if str_num and int(str_num[0]) != patterns_found[0][0] and len(str_num) == 2:
                            points = 25
                else:
                    # Sum every side
                    for i in rolls:
                        if i:
                            points += int(i[0]) * len(i)
        elif pattern_to_find == "small straight":
            patterns = [
                [1, 2, 3, 4],
                [2, 3, 4, 5],
                [3, 4, 5, 6]
            ]

            for pattern in patterns:
                is_found = True
                for num in pattern:
                    if num not in dice_rolls:
                        is_found = False

                if is_found:
                    points = 30
        elif pattern_to_find == "large straight":
            patterns = [
                [1, 2, 3, 4, 5],
                [2, 3, 4, 5, 6],
            ]

            for pattern in patterns:
                is_found = True
                for num in pattern:
                    if num not in dice_rolls:
                        is_found = False

                if is_found:
                    points = 40
        elif pattern_to_find == "chance":
            for i in dice_rolls:
                points += i

    if pattern_to_find == "3 of a kind":
        SCORES[1][0] += points
    elif pattern_to_find == "4 of a kind":
        SCORES[1][1] += points
    else:
        SCORES[1][COUNT_TYPES.index(pattern_to_find)] += points

    return points

def play_game(num_rounds):
    points = 0
    moves_used = []

    for r in range(num_rounds):
        print(f"***** Beginning Round {r+1} *****\n\tYour score is: {get_score(SCORES)}")

        points_awarded = 0
        dice_rolls = roll_dice()
        count_type = input(f"\t{dice_rolls}\n{"How would you like to count this dice roll? "}")

        while count_type in moves_used:
            count_type = input(f"There was already a score in that slot.\n\t{dice_rolls}\n\
{"How would you like to count this dice roll? "}")

        if "count" in count_type:
            # Extract the number the user is trying to count
            count_num = int(count_type.split(" ")[1])
            sides_found = 0

            for i in dice_rolls:
                if i == count_num:
                    sides_found += 1

            points_awarded = count_num * sides_found
            SCORES[0][count_num-1] += points_awarded
        elif count_type != "skip":
            while count_type not in COUNT_TYPES and (count_type != "3 of a kind" and count_type != "4 of a kind"):
                count_type = input("How would you like to count this dice roll? ")

            points_awarded += find_patterns(dice_rolls, count_type)

        if count_type != "pytzee" and count_type != "skip":
            moves_used.append(count_type)

        if points_awarded >= 1:
            print("Accepted the " + count_type)
        else:
            print("No points earned")

        points += points_awarded
        display_scorecard()

    return points

if __name__ == '__main__':
    num_rounds = int(input('What is the number of rounds that you want to play? '))
    seed = int(input('Enter the seed or 0 to use a random seed: '))
    if seed:
        random.seed(seed)
    print(f"Your final score was {play_game(num_rounds)}")