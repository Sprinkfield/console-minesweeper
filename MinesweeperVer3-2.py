from random import randint


def difficulty_choise():
    global size_of_field, repeater, amount_of_mines

    choice = input('Choose difficulty (Easy/Medium/Hard): ').lower()

    if choice == 'easy' or choice.startswith('e'):
        size_of_field = 7
        repeater = 10
        amount_of_mines = 12
    elif choice == 'medium' or choice.startswith('m'):
        size_of_field = 17
        repeater = 50
        amount_of_mines = 99
    elif choice == 'hard' or choice.startswith('h'):
        size_of_field = 27
        repeater = 100
        amount_of_mines = 150
    else:
        print('Error! Please, try again.')
        difficulty_choise()


# Global constants
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NUM_VARS = ['1 |', '2 |', '3 |', '4 |', '5 |', '6 |', '7 |', '8 |']

# Introduction
print('''==========================================
| Welcome!                               |
| This is Console Minesweeper in Python. |
| Input coordinates in format "d2"       |
| Or set a flag by typing "fd2"          |
==========================================
''')


def create_mined_field():
    def add_mine():
        mines_coords = []

        for _ in range(amount_of_mines):
            def loop_placement():

                mine_x = randint(1, size_of_field - 1)
                mine_y = randint(1, size_of_field - 1)

                if [mine_x, mine_y] not in mines_coords:
                    mined_field[mine_x][mine_y] = 1
                    mines_coords.append([mine_x, mine_y])
                else:
                    loop_placement()
            loop_placement()

    mined_field = [[0] * (size_of_field + 1) for _ in range(size_of_field + 1)]

    add_mine()

    for i in range(size_of_field):
        mined_field[0][i] = 2
        mined_field[i][0] = 2
        mined_field[i][size_of_field] = 2
        mined_field[size_of_field - 1][i] = 2

    return mined_field


def create_show_field():
    field = [['• |'] * size_of_field for _ in range(size_of_field)]
    field[0][0] = '  |'

    for element in range(1, size_of_field):
        field[0][element] = ALPHABET[element - 1] + ' |'

    for number in range(1, size_of_field):
                field[number][0] = str(number) + ' |' if number < 10 else str(number) + '|'

    field[size_of_field - 1] = [' ' * 8]

    return field


def check_neighbouring_mines(x_check, y_check):
    counter = 0

    for i in range(y_check - 1, y_check + 2):
        for j in range(x_check - 1, x_check + 2):
            if mined_field[i][j] == 1:
                counter += 1

    return counter


def check_neighbouring_flags(x_check, y_check):
    counter = 0

    for i in range(y_check - 1, y_check + 2):
        for j in range(x_check - 1, x_check + 2):
            if showing_field[i][j] == 'F |':
                counter += 1

    return counter


def check_neighbouring_numbers(x_num, y_num):
    for i in range(y_num - 1, y_num + 2):
        for j in range(x_num - 1, x_num + 2):
            if mined_field[i][j] == 1 and showing_field[i][j] != 'F |':
                game_over()  # End of the game
            if mined_field[i][j] == 0  and showing_field[i][j] != 'F |':
                showing_field[i][j] = str(check_neighbouring_mines(j, i)) + ' |'


def end_game_mines_show():
    for i in range(1, size_of_field):
        for j in range(1, size_of_field):
            if mined_field[i][j] == 1:
                showing_field[i][j] = '# |'

    return showing_field


def clear_field():
    if showing_field[y][x] == '0 |':
        check_neighbouring_numbers(x, y)

        for _ in range(repeater):
            for i in range(1, size_of_field - 1):
                for j in range(1, size_of_field - 1):
                    if showing_field[i][j] == '0 |':
                        check_neighbouring_numbers(j, i)


def game_over():
    for row in end_game_mines_show():
        print(*row)

    print(f'Game Over\n\nPress Enter to exit the game')
    exit(input())  # Exit the game


def mine_check():
    if mined_field[y][x] == 1:
        game_over()  # End of the game
    else:
        showing_field[y][x] = str(check_neighbouring_mines(x, y)) + ' |'

        if showing_field[y][x] in NUM_VARS:
            if str(check_neighbouring_flags(x, y)) + ' |' == showing_field[y][x]:
                check_neighbouring_numbers(x, y)

        clear_field()
        main()


def error_warning():
        print(f'''==========================================
| Error! (Wrong Input) Please try again. |
==========================================
''')


def prevent_game_crashes(x_prevent, y_prevent):
    if str.isnumeric(y_prevent) is True:
        y_prevent = int(y_prevent)
    else:
        error_warning()
        main()

    if (x_prevent.upper() in ALPHABET) and (0 <= y_prevent < size_of_field - 1):
        x_prevent = ALPHABET.index(x_prevent.upper())
        x_prevent += 1
        if x_prevent > size_of_field:
            error_warning()
            main()
        else:
            pass
    else:
        error_warning()
        main()

    return x_prevent, y_prevent


def main():
    for raw in showing_field:
        print(*raw)

    global x, y

    coords_input = input('Input Coordinates: ').lower()
    print()

    if coords_input != 'exit':
        if coords_input != '' and coords_input != 'f':
            if coords_input[0] == 'f' and (len(coords_input) >= 3 and str.isnumeric(coords_input[1]) is False):
                x = coords_input[1]
                y = coords_input[2:]
                x, y = prevent_game_crashes(x, y)

                if showing_field[y][x] == '• |':
                    showing_field[y][x] = 'F |'

                main()
            else:
                x = coords_input[0]
                y = coords_input[1:]
                x, y = prevent_game_crashes(x, y)
        else:
            error_warning()
            main()

        if x < size_of_field:
            mine_check()
        else:
            error_warning()
            main()
    else:
        exit()  # Exit the game

    return x, y


def beginning():
    global mined_field, showing_field

    showing_field = create_show_field()

    for raw in showing_field:
        print(*raw)

    user_input = input('Input Coordinates: ').lower()
    print()

    x = user_input[0]
    y = user_input[1:]

    x, y = prevent_game_crashes(x, y)

    showing_field[y][x] = '0 |'

    if x < size_of_field:
        while True:
            mined_field = create_mined_field()

            if mined_field[y][x] == 0 and check_neighbouring_mines(x, y) == 0:
                break

    for _ in range(repeater):
        for i in range(1, size_of_field - 1):
            for j in range(1, size_of_field):
                if showing_field[i][j] == '0 |':
                    check_neighbouring_numbers(j, i)
    main()


# First steps
difficulty_choise()
beginning()

if __name__ == '__main__':
    main()
