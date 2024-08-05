from .statics import board, cols_names, tags
from typing import Literal

class Connect4:
    '''
    The class of connect 4 game.
    
    ...
    
    Atributes:
    ---------
    __board__ : DataFrame
        The board, in this saves the state of the game
    __last_movements__ : dict
        This save the last move for each row for a easiest access
    __board_movements__ : int
        Save the restant movements in the board before the game are tie
    __marker__ : dict
        The marker of the game
    _player_turn_name_ : str
        Player name on turn
    '''
    
    def __init__(self) -> None:
        self.__clear_board__()
        self.__clear_marker__()
        self.__player_turn__()
    
    
    def __clear_board__(self) -> None:
        'Clear the game board, reset the lasts movements for each column and the board movements'
        self.__board__ = board.copy()
        self.__last_movements__ = {col_name: 6 for col_name in cols_names}
        self.__board_movements__ = 42
        
        
    def __clear_marker__(self) -> None:
        'Sets the marker to 0 for both payers'
        self.__marker__ = {'player1': 0, 'player2': 0}
        
        
    def __print_board__(self) -> None:
        'Print the board'
        print(self.__board__)
        print()
        
        
    def __player_turn__(self) -> None:
        'Sets the players turn if this is not set the player1 are taken else rotate both players'
        self._player_turn_name_ = 'player1' if not hasattr(self, '_player_turn_name_') or self._player_turn_name_ != 'player1' else 'player2'
    
        
    def start_game(self) -> None:
        'Starts the principal loop for the game printing the extra options messages, headers, the board and request the player turn'
        self.__print_options_messages__()
        while True:
            self.__print_headers__()
            self.__print_board__()
            movement = self.__player_movement__()
            
            if not movement:
                break
        
        
    def __print_options_messages__(self) -> None:
        'Paint the extra options messages'
        print('-------------------------------------------------------------')
        print('-----------Para reiniciar el tablero ingresa "limpiar"-------')
        print('-----------Para reiniciar el juego ingresa "nuevo"-----------')
        print('-----------Para salir del juego ingresa "salir"--------------')
        print('-------------------------------------------------------------')
        print()
        
        
    def __print_headers__(self) -> None:
        'Paint the headers: players marker, player turn and option for show extra options'
        print(f'Juagor 1: {self.__marker__["player1"]} | Juagor 2: {self.__marker__["player2"]}')
        print(f'Juega jugador {self._player_turn_name_[-1:]}, ingresa el numero de la columna para agregar la ficha.')
        print('Para ver las opciones adicionales ingresa "opciones"')
        print()
        
        
    def __player_movement__(self) -> bool:
        '''
        Gets the player response and evaluate what is, if are a move in the board proced to execute the validations of the play and realize it
        
        Returns:
            bool: The state of the loop, if it is False stop the aplication else continue
        '''
        # Player response
        player_response = input().lower().replace(' ', '')
        print()
        
        # Stops the game execution
        if player_response == 'salir':
            return False
        
        # Show the extra options
        elif player_response == 'opciones':
            self.__print_options_messages__()
            return True
        
        # Player move
        if player_response not in ['limpiar', 'nuevo']:
            column = f'col {player_response}'
            
            # Validate if the selected column is valid
            if not self.__validate_movement__(column):
                return True
            
            row = f'row {self.__last_movements__[column]}'
            
            # Execute the play
            self.__set_player_movement__(row, column)
            
            # Validate the state of the board
            if self.__validate_board__(int(row[-1:]), int(column[-1:])):
                return True
            
            self.__player_turn__()
            return True
        
        self.__clear_board__()
        self._player_turn_name_ = 'player1'
        
        if player_response == 'nuevo':
            self.__clear_marker__()
            
        return True
    
    
    def __validate_movement__(self, column: str) -> bool:
        '''
        Validate if the column name are valid and if the column are not filled
        
        Returns:
            bool: The response of the validation, if this is False show a error message and request the player play again
        '''
        
        if column not in cols_names:
            print('Error: No has seleccionado una columna valida, intenta de nuevo.')
            return False
        
        if self.__last_movements__[column] == 0:
            print('Error: La columna seleccionada ya esta al maximo, selecciona otra.')
            return False
        
        return True
    
    
    def __set_player_movement__(self, row: str, column: str) -> None:
        '''
        Sets the player turn in the board
        
        Args:
            row (str): row name
            column (str): column name
        '''
        self.__board__.at[row, column] = tags[self._player_turn_name_]
        self.__last_movements__[column] -= 1
        
        
    def __validate_board__(self, row_index: int, col_index: int) -> None:
        '''
        Validate the play searching a winner or tie, if have a tie starts a new game, if have a winner starts a new game and set the win in the marker
        
        Args:
            row_index (int): The index of the played row
            col_index (int): The index of the played column
        '''
        
        # Searchs a horizontal solution
        horizontal = [ self.__check_horizontal_solution__(1, row_index, col_index, direction) for direction in ['<-', '->'] ]
        
        # Searchs a vertical solution
        vertical = self.__check_vertical_solution__(1, row_index, col_index)
        
        # Searchs a oblique solution
        oblique = [ self.__check_oblique_solution__(1, row_index, col_index, direction) for direction in ['<-', '->'] ]

        if (horizontal[0] == 4 or horizontal[1] == 4) or (vertical == 4) or (oblique[0] == 4 or oblique[1] == 4):
            self.__print_board__()
            print(f'Gana el jugador {self._player_turn_name_[-1:]}, iniciando nuevo tablero')
            print()
            
            self.__clear_board__()
            self.__marker__[self._player_turn_name_] += 1
            self._player_turn_name_ = 'player1'
            
            
        self.__board_movements__ -= 1
        if self.__board_movements__ == 0:
            self.__print_board__()
            print('Empate, iniciando nuevo tablero')
            print()
            
            self.__clear_board__()
            self._player_turn_name_ = 'player1'
    
    
    def __check_oblique_solution__(self, counter: int, row_idx: int, col_idx: int, direction: Literal['<-', '->']) -> int:
        '''
        Check a oblique solution, skips the scenarios where are imposible the win, thats are a recursive function
        
        Args:
            counter (int): Counter for all matches of the play
            row_index (int): The index of the played row
            col_index (int): The index of the played column
            direction (Literal["<-", "->"]): The direction to search the solution
            
        Returns:
            int: counter with the matchs
        '''
        row_idx = None if (row_idx >= 4 and counter == 1) else row_idx + 1
        
        if not row_idx or (direction == '->' and col_idx >= 5 and counter == 1) or (direction == '<-' and col_idx <= 3 and counter == 1):
            return counter
        
        operation = '+' if direction == '->' else '-'
        col_idx = int(eval(f'col_idx {operation} 1'))
        
        if self.__board__.at[f'row {row_idx}', f'col {col_idx}'] != tags[self._player_turn_name_]:
            return counter
        
        counter += 1
        if counter == 4:
            return counter
        
        return self.__check_oblique_solution__(counter, row_idx, col_idx, direction)


    def __check_horizontal_solution__(self, counter: int, row_idx: int, col_idx: int, direction: Literal['<-', '->']) -> int:
        '''
        Check a horizontal solution, skips the scenarios where are imposible the win, thats are a recursive function
        
        Args:
            counter (int): Counter for all matches of the play
            row_index (int): The index of the played row
            col_index (int): The index of the played column
            direction (Literal["<-", "->"]): The direction to search the solution
            
        Returns:
            int: counter with the matchs
        '''
        if (direction == '->' and col_idx >= 5 and counter == 1) or (direction == '<-' and col_idx <= 3 and counter == 1):
            return counter
        
        operation = '+' if direction == '->' else '-'
        col_idx = int(eval(f'col_idx {operation} 1'))
        
        if self.__board__.at[f'row {row_idx}', f'col {col_idx}'] != tags[self._player_turn_name_]:
            return counter
        
        counter += 1
        if counter == 4:
            return counter
        
        return self.__check_horizontal_solution__(counter, row_idx, col_idx, direction)


    def __check_vertical_solution__(self, counter: int, row_idx: int, col_idx: int) -> int:
        '''
        Check a vertical solution, skips the scenarios where are imposible the win, thats are a recursive function
        
        Args:
            counter (int): Counter for all matches of the play
            row_index (int): The index of the played row
            col_index (int): The index of the played column
            
        Returns:
            int: counter with the matchs
        '''
        if (row_idx >= 4 and counter == 1):
            return counter
        
        row_idx += 1
        if self.__board__.at[f'row {row_idx}', f'col {col_idx}'] != tags[self._player_turn_name_]:
            return counter
        
        counter += 1
        if counter == 4:
            return counter
        
        return self.__check_vertical_solution__(counter, row_idx, col_idx)
