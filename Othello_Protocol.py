class InvalidMove(Exception):
    None
class WinningSequence(Exception):
    None
class Othello:
    def __init__(self,  row: int, column: int, turn:str):
        '''Initiates the Othello game. Gamestate checks whether or not a game is finished.
If it reaches 2, then there are no more available moves. Else, there are still available moves.'''
        self._row = row 
        self._col = column 
        self._board = self._create_board()
        self._turn = turn
        self._gamestate = 0
        self._wscore = 0
        self._bscore = 0
        self._winner = None
    def _create_board(self) -> [[str]]:
        '''Automatically creates a board based on the rows and columns
given by the init once the class is initialized'''
        board = []
        for row in range(self._row):
            board.append([])
            for col in range(self._col):
                board[-1].append([row,col])
        return board
    
    def new_game_board(self, choice:str) -> [[str]]:
        '''Creates a game board. If the function is given W, then White will be an the top
rught corner. If given B, than black will be.'''
        if choice == 'W':
            tile = 'W'
            alttile = 'B'
        else:
            tile = 'B'
            alttile = 'W'
            
        self._board[int(self._row//2)][int(self._col//2)] = tile
        self._board[int((self._row//2-1))][int((self._col//2)-1)] = tile
        self._board[int((self._row//2)-1)][int(self._col//2)] = alttile
        self._board[int(self._row//2)][int((self._col//2)-1)] = alttile
    def gameboard(self)->[list]:
        '''Returns current gameboard'''
        return self._board
    def change_turn(self) -> str:
        '''Changes the player turn'''
        if self._turn == 'W':
            self._turn = 'B'
        else:
            self._turn = 'W'

    def return_turn(self) -> str:
        '''returns the current player'''
        if self._turn == 'W':
            return 'White'
        else:
            return 'Black'
        

    def opposite_player(self)->str:
        '''Gives the opposite player of the current player'''
        if self._turn == 'W':
            return 'B'
        else:
            return 'W'

        
    def drop_piece(self, row:int, col:int) -> [[str]]:
        '''Function that enacts the game logic that changes the pieces to the
current players. Then, it changes to the other players turn and counts score of the
current board. If a coordinate already has a piece and/or the move flips no pieces, raises
InvalidMove exception'''
        row = row
        col = col
        if type(self._board[row][col]) == str:
            raise InvalidMove
        if self._move_checker(row, col) == []:
            raise InvalidMove
        self._board[row][col] = self._turn
        self._flip_pieces(self._move_checker(row, col))
        self.change_turn()
        self._score_counter()
        
    
    def _directional_checker(self, row:int, col:int, deltarow:int, deltacol:int) -> [list]:
        '''Takes a coordinate and a direction checks if the row in that coordinate's direction
will be able to change pieces. If it can, it returns a list of pieces that can be switched. If not,
then it returns an empty list.'''
        tilestoflip = []
        i = 1
        while self._check_on_board(row+deltarow*i, col+deltacol*i):
            if self._board[row+deltarow*i][col+deltacol*i] == self.opposite_player():
                tilestoflip.append(self._create_board()[row+deltarow*i][col+deltacol*i])
            elif self._board[row+deltarow*i][col+deltacol*i] == self._turn:
                tilestoflip.append(self._create_board()[row+deltarow*i][col+deltacol*i])
                break
            else:
                break
            i += 1

        if tilestoflip == []:
            return []
        elif self._converter(tilestoflip[-1]) == self._turn and [coordinate for coordinate in tilestoflip[:-1] if self._converter(coordinate) == self.opposite_player()]:
            return tilestoflip
        else:
            return []

    def _move_checker(self, row:int, col:int)->[list]:
        '''Applies the _directional_checker function to all 8 directions. Combines the lists
given by the results of applying all 8 directions to the function. Returns the combined list.'''
        tilestoflip = []
        tilestoflip.extend(self._directional_checker(row, col, 1,1))
        tilestoflip.extend(self._directional_checker(row, col, 1,0))
        tilestoflip.extend(self._directional_checker(row, col, 0,1))
        tilestoflip.extend(self._directional_checker(row, col, 0,-1))
        tilestoflip.extend(self._directional_checker(row, col, -1,0))
        tilestoflip.extend(self._directional_checker(row, col, -1,1))
        tilestoflip.extend(self._directional_checker(row, col, 1,-1))
        tilestoflip.extend(self._directional_checker(row, col, -1,-1))
        if tilestoflip == []:
            return []
        else:
            return tilestoflip
        
    def _flip_pieces(self, tilestoflip: [list])->None:
        '''changes a list of coordinates into the current players pieces.'''
        for coordinate in tilestoflip:
            x = coordinate[0]
            y = coordinate[1]
            self._board[x][y] = self._turn
    def check_for_valid_moves(self)->[list]:
        '''Checks if the current player player has any valid moves. If not,
changes player and add's 1 to the gamestate. If there are resets the game state
to 0'''
        opencoordinates = []
        check = []
        for row in self._board:
            for col in row:
                if type(col) != str:
                    check.append(col)
        for coordinate in check:
            x = coordinate[0]
            y = coordinate[1]
            opencoordinates += self._move_checker(x, y)
        if opencoordinates == []:
            self._gamestate += 1
            self.change_turn()
        else:
            self._reset_game_state()
    def end_check(self)->None:
        '''Checks to see whether or not to end the game. If gamestate reaches 2, that means
both players cannot make a move. Therefore, a WinningSequence exception is raised.'''
        if self._gamestate == 2:
            raise WinningSequence
    def _score_counter(self)->None:
        '''Changes the White sSore(self._wscore) and the Black Score(self._bscore) to the
current board's score'''
        white_score = 0
        black_score = 0
        for row in self._board:
            for col in row:
                if col == 'W':
                    white_score += 1
                elif col == 'B':
                    black_score += 1
        self._wscore = white_score
        self._bscore = black_score
    def decide_winner(self, mode: str):
        '''Compares white and black score and decides winner based on the most pieces.'''
        if mode == 'W':
            if self._wscore > self._bscore:
                self._winner = 'White'
            elif self._bscore > self._wscore:
                self._winner = 'Black'
        else:
                
            if self._wscore < self._bscore:
                self._winner = 'White'
            elif self._bscore < self._wscore:
                self._winner = 'Black'

    def _converter(self, coordinate: [list]) ->str:
        '''Returns the tile of the given coordinate'''
        x = coordinate[0]
        y = coordinate[1]
        return self._board[x][y]
            
    def _reset_game_state(self)->None:
        '''Resets the game state to 0'''
        self._gamestate = 0

    def return_w_score(self)->int:
        '''returns White score'''
        return self._wscore

    def return_b_score(self)->int:
        '''returns Black score'''
        return self._bscore
    
    def return_game_winner(self)->str:
        '''Returns winner'''
        return self._winner
                
    def _check_on_board(self, row: int, col:int)->bool:
        '''Checks if a coordinate is on the board'''
        return row >= 0 and row < self._row and col >=0 and col < self._col
    
        
    

        
        
        







