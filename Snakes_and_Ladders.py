from collections import deque, defaultdict, Counter

class SnakeAndLaddersGame:
    def __init__(self, board_size, snakes, ladders):
        self.board_size = board_size
        self.snakes = snakes
        self.ladders = ladders
        self.board = defaultdict(list)
        
    def construct_board(self):
        for position in range(1, self.board_size * self.board_size + 1):
            if position in self.snakes:
                self.board[position].append(self.snakes[position])
            elif position in self.ladders:
                self.board[position].append(self.ladders[position])
            else:
                for dice_roll in range(1, 7):
                    new_position = position + dice_roll
                    if new_position <= self.board_size * self.board_size:
                        self.board[position].append(new_position)
    
    def find_shortest_distance(self):
        distances = [-1] * (self.board_size * self.board_size + 1)
        distances[1] = 0
        queue = deque([1])

        while queue:
            current_position = queue.popleft()
            for neighbor_position in self.board[current_position]:
                if distances[neighbor_position] == -1:
                    distances[neighbor_position] = distances[current_position] + 1
                    queue.append(neighbor_position)

        if distances[self.board_size * self.board_size] == -1:
            return -1  # If the end is unreachable
        else:
            return distances[self.board_size * self.board_size]

    def has_cycles(self):
        snake_tails = set(self.snakes.values())
        ladder_bottoms = set(self.ladders.keys())
        snake_heads = set(self.snakes.keys())
        ladder_heads = set(self.ladders.values())
        return bool(snake_tails & ladder_bottoms) or bool(snake_heads & ladder_heads)

    def has_direct_ladder(self):
        return any(start == 1 and end == self.board_size * self.board_size for start, end in self.ladders.items())

    def is_valid(self):
        unique_positions = set(self.snakes.keys()) | set(self.ladders.keys())
        duplicate_snakes = [item for item, count in Counter(self.snakes.values()).items() if count > 1]
        duplicate_ladders = [item for item, count in Counter(self.ladders.values()).items() if count > 1]

        if duplicate_snakes or duplicate_ladders:
            print("Duplicate snakes or ladders found:", duplicate_snakes, duplicate_ladders)
            return False

        return len(unique_positions) == len(self.snakes) + len(self.ladders)

    def find_duplicates(self):
        duplicate_snakes = [item for item, count in Counter(self.snakes.values()).items() if count > 1]
        duplicate_ladders = [item for item, count in Counter(self.ladders.values()).items() if count > 1]

        if duplicate_snakes:
            print("Duplicate snakes found:", duplicate_snakes)
        else:
            print("No duplicate snakes found.")

        if duplicate_ladders:
            print("Duplicate ladders found:", duplicate_ladders)
        else:
            print("No duplicate ladders found.")

def get_user_input(prompt):
    return int(input(prompt))

def get_snakes_or_ladders_input(label, num_items):
    data = {}
    for i in range(num_items):
        start = get_user_input(f"Enter the position for {label} {i + 1}: ")
        end = get_user_input(f"Enter the position for {label} {i + 1}: ")
        data[start] = end
    return data

# Input from users
n = get_user_input("Enter the board size: ")
num_snakes = get_user_input("Enter the number of snakes: ")
snakes = get_snakes_or_ladders_input("snake", num_snakes)

num_ladders = get_user_input("Enter the number of ladders: ")
ladders = get_snakes_or_ladders_input("ladder", num_ladders)

# Create the game
game = SnakeAndLaddersGame(n, snakes, ladders)
game.construct_board()

game.find_duplicates()

shortest_distance = game.find_shortest_distance()
print(f"The shortest distance to traverse the board is {shortest_distance} steps.")

if game.has_cycles():
    print("The game configuration has loop.")
else:
    print("The game configuration does not have loop.")
    
if game.has_direct_ladder():
    print("The game has a ladder from start to the end.")
else:
    print("The game does not have a ladder from start to the end.")
    
if game.is_valid():
    print("The game board has a valid configuration.")
else:
    print("The game board does not have a valid configuration.")
