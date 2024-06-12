import random

SIZE = 9
SUBGRID = 3
EMPTY = 0
solved_board = None

def generate_board(empty_cells):
    board = [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]
    fill_diagonal_subgrids(board)
    solve_sudoku(board)
    global solved_board
    solved_board = [row[:] for row in board]
    remove_elements(board, empty_cells)
    return board

def fill_diagonal_subgrids(board):
    for i in range(0, SIZE, SUBGRID):
        fill_subgrid(board, i, i)

def fill_subgrid(board, row, col):
    nums = list(range(1, SIZE + 1))
    random.shuffle(nums)
    for i in range(SUBGRID):
        for j in range(SUBGRID):
            board[row + i][col + j] = nums.pop()

def solve_sudoku(board):
    empty = find_empty_location(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, SIZE + 1):
        if is_safe(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = EMPTY
    return False

def is_safe(board, row, col, num):
    return not is_in_row(board, row, num) and not is_in_col(board, col, num) and not is_in_subgrid(board, row - row % SUBGRID, col - col % SUBGRID, num)

def is_in_row(board, row, num):
    return num in board[row]

def is_in_col(board, col, num):
    return num in [board[row][col] for row in range(SIZE)]

def is_in_subgrid(board, start_row, start_col, num):
    for row in range(SUBGRID):
        for col in range(SUBGRID):
            if board[row + start_row][col + start_col] == num:
                return True
    return False

def remove_elements(board, count):
    while count > 0:
        row = random.randint(0, SIZE - 1)
        col = random.randint(0, SIZE - 1)
        if board[row][col] != EMPTY:
            board[row][col] = EMPTY
            count -= 1

def is_solved(board):
    return all(all(cell != EMPTY for cell in row) for row in board)

def is_valid_move(board, row, col, num):
    return board[row][col] == EMPTY and is_safe(board, row, col, num)

def print_board(board):
    for row in range(SIZE):
        if row % SUBGRID == 0 and row != 0:
            print("----+---------+---------+----")
        for col in range(SIZE):
            if col % SUBGRID == 0 and col != 0:
                print("|", end="")
            print(" {} ".format(board[row][col] if board[row][col] != EMPTY else " "), end="")
        print()

def find_empty_location(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                return (row, col)
    return None

def main():
    import sys
    play_again = True

    while play_again:
        # Choose difficulty level
        print("Select difficulty level: easy, medium, hard")
        level = input().strip().lower()
        if level == "easy":
            empty_cells = 20
        elif level == "medium":
            empty_cells = 40
        elif level == "hard":
            empty_cells = 60
        else:
            print("Invalid level. Defaulting to easy.")
            empty_cells = 20

        board = generate_board(empty_cells)
        print_board(board)

        while not is_solved(board):
            print("Enter your move (row column number), 'answer' to see the solution, or 'exit' to quit:")
            user_input = input().strip().lower()

            if user_input == "exit":
                print("Goodbye!")
                sys.exit()
            elif user_input == "answer":
                print_board(solved_board)
                break

            try:
                parts = user_input.split()
                row = int(parts[0]) - 1
                col = int(parts[1]) - 1
                num = int(parts[2])

                if is_valid_move(board, row, col, num):
                    board[row][col] = num
                    print_board(board)
                else:
                    print("Invalid move. Try again.")
            except Exception as e:
                print("Invalid input. Please enter row, column, and number separated by spaces.")

        if is_solved(board):
            print("Congratulations! You solved the Sudoku puzzle.")

        print("Would you like to play again? (yes/no)")
        play_again = input().strip().lower() == "yes"

    print("Thanks for playing! Goodbye.")

if __name__ == "__main__":
    main()
