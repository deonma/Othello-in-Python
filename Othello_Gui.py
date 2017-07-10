import tkinter
import InputDialog
import Othello_Protocol
DEFAULT_FONT = ('Helvetica', 14)


class Othello_Gui:
    def __init__(self):
        '''Asks users if they want to play othello and stores all the information
for the game logic.'''
        self._root_window = tkinter.Tk()
        self.othello_button = tkinter.Button(
            master = self._root_window, text = 'Play Othello?', font = DEFAULT_FONT,
            command = self._on_play_othello)

        self.othello_button.grid(
            row = 0, column = 0, padx = 10, pady = 10,
            sticky = tkinter.N)
        self._game_logic = None
        self._board = None
        self._dialog = None
        self._mode = None
        self._canvas = None
        self._rows = None
        self._col = None
        self._wscore = None
        self._bscore = None
        self._turn = None

       
 
    def start(self)->None:
        '''Starts the window for the Othello game.'''
        self._root_window.mainloop()
    def _on_play_othello(self) -> None:
        '''If play othello was clicked, a window pops up asking for user inputs. Once ok
is pressed all the user inputs are saved and implemented in the game logic. The board is then
printed and the game is started.'''
        dialog = InputDialog.InputDialog()
        self._dialog = dialog
        dialog.show()
        if dialog.was_ok_clicked():
            self.othello_button.destroy()
            self._game_logic = \
                             Othello_Protocol.Othello(dialog.get_row(), dialog.get_col(), dialog.get_first_player())
            self._game_logic.new_game_board(dialog.get_top_left())
            self._board = self._game_logic.gameboard()
            self._wscore = self._game_logic.return_w_score()
            self._bscore = self._game_logic.return_b_score()
            self._turn = self._game_logic.return_turn()
            self._mode = dialog.get_game_mode()
            self._wscoretext = tkinter.StringVar()
            self._wscoretext.set('White Score: {}'.format(self._wscore))
            self._wscore_label = tkinter.Label(
                master = self._root_window, textvariable = self._wscoretext,font = DEFAULT_FONT)

            self._wscore_label.grid(
                row = 0, column = 0, columnspan = 2, padx = 10, pady = 10,sticky = tkinter.NSEW)
            self._bscoretext = tkinter.StringVar()
            self._bscoretext.set('Black Score: {}'.format(self._bscore))

            self._bscore_label = tkinter.Label(
                master = self._root_window, textvariable = self._bscoretext,font = DEFAULT_FONT)

            self._bscore_label.grid(
                row = 1, column = 0, columnspan = 2, padx = 10, pady = 10,sticky = tkinter.NSEW)
            self._turntext = tkinter.StringVar()
            self._turntext.set('Current Turn: {}'.format(self._turn))

            self._turn_label = tkinter.Label(
                master = self._root_window, textvariable = self._turntext,font = DEFAULT_FONT)

            self._turn_label.grid(
                row = 2, column = 0, columnspan = 2, padx = 10, pady = 10,sticky = tkinter.NSEW)

            self._rows = self._dialog.get_row()
            self._col = self._dialog.get_col()
            self.create_board()
            self._canvas.bind('<Configure>', self._on_canvas_resized)
            self._canvas.bind('<Button-1>', self._on_canvas_clicked)
            
                 
    def create_board(self) ->None:
        '''Creates the starting game board for Othello.'''
        rows = self._rows
        cols = self._col
        widths = rows*50
        heights = cols*50       
        self._canvas = tkinter.Canvas(
            master = self._root_window,width=widths,height=heights,background='black')
        self._canvas.grid(
            row = 3, column = 0, columnspan = 1, padx = 10, pady = 10,
            sticky =tkinter.NSEW)
        self._root_window.rowconfigure(3, weight = 1) 
        self._root_window.columnconfigure(0, weight = 1)
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()
       
        for row in range(rows):
            for col in range(cols):
                x0 = row * 50
                y0 = col * 50
                x1 = x0 + 50
                y1 = y0 + 50
                self._canvas.create_rectangle(x0, y0, x1,y1, fill="#228B22")
                if type(self._board[row][col]) != list:
                    if self._board[row][col] == 'W':
                        piece = 'white'
                    elif self._board[row][col] == 'B':
                        piece = 'black'
                    self._canvas.create_oval(x0, y0, x1, y1, fill=piece) 
    def _on_canvas_resized(self, event: tkinter.Event)->None:
        '''Is called when the window size is changed and resizes the board accordingly.'''
        self.draw_board()
    def draw_board(self)->None:
        '''Redraws the board based on the current state of the game board based on the game logic.'''
        self._canvas.delete(tkinter.ALL)
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()
        rows = self._rows
        cols = self._col
        for row in range(rows):
            for col in range(cols):
                x0 = row * (canvas_width/rows)
                y0 = col * (canvas_height/cols)
                x1 = x0 + (canvas_width/rows)
                y1 = y0 + (canvas_height/cols)
                self._canvas.create_rectangle(x0, y0, x1, y1, fill="#228B22")
                if type(self._board[row][col]) != list:
                    if self._board[row][col] == 'W':
                        piece = 'white'
                    elif self._board[row][col] == 'B':
                        piece = 'black'
                    self._canvas.create_oval(x0, y0, x1, y1, fill=piece)
    def _on_canvas_clicked(self, event: tkinter.Event):
        '''Changes the game logic board based on where the user clicked on the board.
if the click is within the parameters of a box, it changes that place on the board into
the users picece. Then it checks whether there are any more moves on the board and if the game is
over. Also it chages the the score and turn of the labels.If the user makes an invlaid move,
nothing happens. If the game is over, the turn label changes to whoever is the winner'''
        try:

            canvas_width = self._canvas.winfo_width()
            canvas_height = self._canvas.winfo_height()
            rows = self._rows
            cols = self._col
            for row in range(rows):
                for col in range(cols):
                    x0 = row * (canvas_width/rows)
                    y0 = col * (canvas_height/cols)
                    x1 = x0 + (canvas_width/rows)
                    y1 = y0 + (canvas_height/cols)        
                    if x0 <= event.x and x1 >= event.x\
                       and y0 <= event.y and y1 >= event.y:
                            self._game_logic.drop_piece(row, col)
                            self.draw_board()
                            self._wscore = self._game_logic.return_w_score()
                            self._bscore = self._game_logic.return_b_score()
                            self._turn = self._game_logic.return_turn()
                            self._wscoretext.set('White Score: {}'.format(self._wscore))
                            self._bscoretext.set('Black Score: {}'.format(self._bscore))
                            self._turntext.set('Current Turn: {}'.format(self._turn))
                            self._game_logic.check_for_valid_moves()
                            self._turn = self._game_logic.return_turn()
                            self._turntext.set('Current Turn: {}'.format(self._turn))
                            self._game_logic.check_for_valid_moves()
                            self._game_logic.end_check()
            
        except Othello_Protocol.WinningSequence:
            self._game_logic.decide_winner(self._mode)
            if self._game_logic.return_game_winner() != None:
                self._turntext.set('The Winner is Player {}!'.format(self._game_logic.return_game_winner()))
            else:

                self._turntext.set("Tie Game!")
            self.othello_button = tkinter.Button(
                master = self._root_window, text = 'Play Again?', font = DEFAULT_FONT,command = self._on_play_othello)
            self.othello_button.grid(
                row = 4, column = 0, padx = 10, pady = 10, sticky = tkinter.NS)

        except Othello_Protocol.InvalidMove:
            pass


if __name__ == '__main__':
    Othello_Gui().start()
