import tkinter
DEFAULT_FONT = ('Helvetica', 14)
class InputDialog:
    def __init__(self):
        '''Initiaites the class by asking users for the amount of rows and columns,
the game mode , which color is first, and the color of the top right in the startingcenter pieces.'''
        
        self._dialog_window = tkinter.Toplevel()


        size_label = tkinter.Label(
            master = self._dialog_window, text = 'Create Board Size',
            font = DEFAULT_FONT)

        size_label.grid(
            row = 0, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W)

        row_label = tkinter.Label(
            master = self._dialog_window, text = 'Row Size(even integer 4-16):',
            font = DEFAULT_FONT)

        row_label.grid(
            row = 1, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._row_entry = tkinter.Entry(
            master = self._dialog_window, width = 20, font = DEFAULT_FONT)

        self._row_entry.grid(
            row = 1, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)

        col_label = tkinter.Label(
            master = self._dialog_window, text = 'Column Size(even integer 4-16):',
            font = DEFAULT_FONT)

        col_label.grid(
            row = 2, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._col_entry = tkinter.Entry(
            master = self._dialog_window, width = 20, font = DEFAULT_FONT)

        self._col_entry.grid(
            row = 2, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)

        mode_label = tkinter.Label(
            master = self._dialog_window, text = 'Choose Game Mode:',
            font = DEFAULT_FONT)

        mode_label.grid(
            row = 4, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W)        
        
        self._buttonvar = tkinter.IntVar()
        most_button = tkinter.Radiobutton(
            master = self._dialog_window, text='Most Pieces', variable=self._buttonvar,
            value=1)
        most_button.grid(
            row = 5, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        least_button = tkinter.Radiobutton(
            master = self._dialog_window, text='Least Pieces', variable=self._buttonvar,
            value=2)
                                          
        least_button.grid(
            row = 5, column = 1, padx = 10, pady = 10,
            sticky = tkinter.W)

        player_label = tkinter.Label(
            master = self._dialog_window, text = 'Who should go first?',
            font = DEFAULT_FONT)

        player_label.grid(
            row = 6, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W)        
        
        self._playervar = tkinter.IntVar()
        most_button = tkinter.Radiobutton(
            master = self._dialog_window, text='White', variable=self._playervar,
            value=1)
        most_button.grid(
            row = 7, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        least_button = tkinter.Radiobutton(
            master = self._dialog_window, text='Black', variable=self._playervar,
            value=2)
                                          
        least_button.grid(
            row = 7, column = 1, padx = 10, pady = 10,
            sticky = tkinter.W)

        board_label = tkinter.Label(
            master = self._dialog_window, text = 'What piece should be on the top left?',
            font = DEFAULT_FONT)

        board_label.grid(
            row = 8, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W)        
        
        self._topleftvar = tkinter.IntVar()
        most_button = tkinter.Radiobutton(
            master = self._dialog_window, text='White', variable=self._topleftvar,
            value=1)
        most_button.grid(
            row = 9, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        least_button = tkinter.Radiobutton(
            master = self._dialog_window, text='Black', variable=self._topleftvar,
            value=2)
                                          
        least_button.grid(
            row = 9, column = 1, padx = 10, pady = 10,
            sticky = tkinter.W)
       

        button_frame = tkinter.Frame(master = self._dialog_window)

        button_frame.grid(
            row = 10, column = 1, padx = 10, pady = 10,
            sticky = tkinter.E + tkinter.S)
 

        ok_button = tkinter.Button(
            master = button_frame, text = 'OK', font = DEFAULT_FONT,
            command = self._on_ok_button)

        ok_button.grid(row = 0, column = 0, padx = 10, pady = 10)

        cancel_button = tkinter.Button(
            master = button_frame, text = 'Cancel', font = DEFAULT_FONT,
            command = self._on_cancel_button)

        cancel_button.grid(row = 0, column = 1, padx = 10, pady = 10)
        
        
        self._dialog_window.rowconfigure(3, weight = 1)
        self._dialog_window.columnconfigure(1, weight = 1)
        self._ok_clicked = False
        self._row = None
        self._col = None
        self._game_mode = None
        self._first_player = None
        self._top_left = None

        
    def show(self) -> None:
        '''Shows the window that asks users for the inputs'''
        self._dialog_window.grab_set()
        self._dialog_window.wait_window()

    def was_ok_clicked(self) -> bool:
        '''Returns true if ok was clicked. Fakse otherwise.'''
        return self._ok_clicked

    def get_game_mode(self) ->str:
        '''Returns the user inputted game mode'''
        return self._game_mode
    def get_first_player(self) ->str:
        '''Returns users inputted first player.'''
        return self._first_player
    def get_top_left(self) ->str:
        '''Returns user inputted top left.'''
        return self._top_left
    def get_col(self) -> str:
        '''Returns user inputted number of columns'''
        return self._col


    def get_row(self) -> str:
        '''Returns user inputted number of rows'''
        return self._row

               
    def _on_ok_button(self) -> None:
        '''Sets the universal values of the init to the user inputs. If the user inputs
are not acceptable, ok does nothing.'''
        try:
            if int(self._buttonvar.get()) == 1:
                self._game_mode = 'W'
            elif int(self._buttonvar.get()) == 2:
                self._game_mode = 'B'

            if int(self._playervar.get()) == 1:
                self._first_player = 'W'
            elif int(self._playervar.get()) == 2:
                self._first_player = 'B'

            if int(self._topleftvar.get()) == 1:
                self._top_left = 'W'
            elif int(self._topleftvar.get()) == 2:
                self._top_left = 'B'
            
            if int(self._row_entry.get()) >= 4 \
            and int(self._col_entry.get()) >= 4 \
            and int(self._row_entry.get()) <= 16 \
            and int(self._col_entry.get()) <= 16 \
            and int(self._row_entry.get())%2 == 0 \
            and int(self._col_entry.get())%2 == 0 \
            and int(self._buttonvar.get()) != 0 \
            and int(self._playervar.get()) != 0 \
            and int(self._topleftvar.get()) != 0:
                self._row = int(self._row_entry.get())
                self._col = int(self._col_entry.get())
                self._ok_clicked = True
                self._dialog_window.destroy()
        except:
            pass


    def _on_cancel_button(self) -> None:
        '''When cancel button is pressed the window closes and nothing happens.'''
        self._dialog_window.destroy()
