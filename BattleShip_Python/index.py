import random

# Define the sizes of the ships and the game board dimensions
SHIP_SIZES = [2,3,3,4,5]  
BOARD_SIZE = 8

# Set up the game boards for the player and computer
player_board = [[" "] * BOARD_SIZE for _ in range(BOARD_SIZE)]
computer_board = [[" "] * BOARD_SIZE for _ in range(BOARD_SIZE)]
player_guess_board = [[" "] * BOARD_SIZE for _ in range(BOARD_SIZE)]
computer_guess_board = [[" "] * BOARD_SIZE for _ in range(BOARD_SIZE)]

# Dictionary to map letters to numbers for user input
letter_to_number = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7}

def print_board(board):
    """This function prints the game board. Used for debugging and for player to see their ships."""
    print("  A B C D E F G H")
    print("  +-+-+-+-+-+-+-+")
    row_number = 1
    for row in board:
        print("%d|%s|" % (row_number, "|".join(row)))
        row_number += 1

def place_ships(board):
    """This function places the ships on the given board. If the board belongs to the computer, placements are random."""
    
    for ship_length in SHIP_SIZES:
        
        while True:
            if board == computer_board:
                orientation, row, column = random.choice(["H", "V"]), random.randint(0,BOARD_SIZE-1), random.randint(0,BOARD_SIZE-1)
                if check_ship_fit(ship_length, row, column, orientation):
                  
                    if not ship_overlaps(board, row, column, orientation, ship_length):
                       
                        if orientation == "H":
                            for i in range(column, column + ship_length):
                                board[row][i] = "X"
                        else:
                            for i in range(row, row + ship_length):
                                board[i][column] = "X"
                        break
            else:
                print('Time to place your ship with a length of ' + str(ship_length) + ' on your board.')
                row, column, orientation = user_input(True)
                if check_ship_fit(ship_length, row, column, orientation):
                    
                        if not ship_overlaps(board, row, column, orientation, ship_length):
                      
                            if orientation == "H":
                                for i in range(column, column + ship_length):
                                    board[row][i] = "X"
                            else:
                                for i in range(row, row + ship_length):
                                    board[i][column] = "X"
                            print('This is your board right now:')
                            print_board(player_board)
                            break 

def check_ship_fit(ship_length, row, column, orientation):
    """This function checks if the ship fits on the board given its proposed location and orientation."""
    if orientation == "H":
        return column + ship_length <= BOARD_SIZE
    else:
        return row + ship_length <= BOARD_SIZE

def ship_overlaps(board, row, column, orientation, ship_length):
    """This function checks if the ship overlaps any other ships on the board."""
    if orientation == "H":
        for i in range(column, column + ship_length):
            if board[row][i] == "X":
                return True
    else:
        for i in range(row, row + ship_length):
            if board[i][column] == "X":
                return True
    return False

def user_input(place_ship):
    """This function handles user input and validation."""
    orientation = get_input("Enter orientation (H or V): ", str, ['H', 'V'])
    row = get_input("Enter the row (1-8) of the ship: ", int, range(1, BOARD_SIZE + 1)) - 1
    column = get_input("Enter the column (A-H) of the ship: ", str, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
    column = letter_to_number[column]
    return row, column, orientation 

def get_input(prompt, type_=None, range_=None, list_=None):
    """This function handles the validation of user inputs."""
    value = ''
    while True:
        value = input(prompt)
        if type_ is not None:
            try:
                value = type_(value)
            except ValueError:
                print(f"Invalid input. Expected type {type_.__name__}.")
                continue
        if range_ is not None and value not in range_:
            print(f"Invalid input. Expected values in range {range_}.")
            continue
        if list_ is not None and value not in list_:
            print(f"Invalid input. Expected values in {list_}.")
            continue
        break
    return value

def count_hit_ships(board):
    """This function counts the number of ships hit on a board."""
    count = 0
    for row in board:
        for column in row:
            if column == "X":
                count += 1
    return count

def turn(board, is_player=False):
    """This function handles a turn for either the player or the computer."""
    while True:
        row, column = user_input(False) if is_player else (random.randint(0,BOARD_SIZE-1), random.randint(0,BOARD_SIZE-1))
        if board[row][column] not in ["-", "X"]:
            board[row][column] = "X" if (player_board if is_player else computer_board)[row][column] == "X" else "-"
            break

print("\n======= Welcome to Battleship =======\n\n")

place_ships(computer_board)
print('This is your empty board. Time to place your ships!')
print_board(player_board)
place_ships(player_board)

while True:
    # Player turn
    print("\n -- Your Turn --\n")
    print('Guess a location on the enemy board.')
    print_board(player_guess_board)
    turn(player_guess_board, True)
    if count_hit_ships(player_guess_board) == sum(SHIP_SIZES):
        print("Congratulations! You have won the game!")
        break   
    
    # Computer turn
    print("\n-- Computer's Turn --\n")
    turn(computer_guess_board)
    print('The computer made a move.')
    if count_hit_ships(computer_guess_board) == sum(SHIP_SIZES):
        print("Unfortunately, the computer has won the game. Better luck next time.")
        break
