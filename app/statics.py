from pandas import DataFrame

# Generate the columns names
cols_names = [f'col {c}' for c in range(1,8)]

# Generate the inicial board game
board = DataFrame({f'col {c}': ['-' for _ in range(0,6)] for c in range(1,8)}, index=[f'row {r}' for r in range(1,7)])

# Sets the tags for each player
tags = {'player1': 'X', 'player2': 'O'}