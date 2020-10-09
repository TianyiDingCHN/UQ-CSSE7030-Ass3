"""
Graphical User Interface (GUI) for Pokemon Game

When this script is run, it will show a board which you can play a Catch Pokemon Game

Some code are come form:
https://learn.uq.edu.au/webapps/blackboard/content/listContent.jsp?course_id=_128547_1&content_id=_5017694_1

"""


"""
import useful packages
"""
import tkinter as tk
import random
from tkinter import messagebox
import time
import linecache
from tkinter import filedialog
from PIL import ImageTk, Image


"""
define some useful variables
"""
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
DIRECTIONS = (UP, DOWN, LEFT, RIGHT,
              f"{UP}-{LEFT}", f"{UP}-{RIGHT}",
              f"{DOWN}-{LEFT}", f"{DOWN}-{RIGHT}")
POKEMON = "☺"
FLAG = "♥"
UNEXPOSED = "~"


class BoardModel(object):
    """
    This part will be used to store and manage the internal game state

    There will have some code from Assignment 1
    """

    def __init__(self, grid_size, num_pokemon):
        """
        Construct the basic model of Pokemon Game

        Args:
            grid_size: the board size of the game
            num_pokemon: how many pokemons in this game
        """

        self._grid_size = grid_size
        self._num_pokemon = num_pokemon
        self._game_string = None
        self._pokemon_locations = None
        self.get_game()
        self.get_pokemon_locations()

    def get_game(self):
        """ Return the game string when input the grid size."""
        game_string = UNEXPOSED * self._grid_size ** 2

        self._game_string = game_string
        return self._game_string

    def restart_game(self):
        """ Reset the game string but no not change the pokemon locations."""
        return self.get_game()

    def new_game(self):
        """ Reset the pokemon locations for a new game. """
        return self.get_pokemon_locations()

    def get_pokemon_locations(self):

        """
        Pokemons will be generated and given a random index within the game.

        And update the value of self._pokemon_locations

        """
        cell_count = self._grid_size ** 2
        pokemon_locations = ()

        for _ in range(self._num_pokemon):
            if len(pokemon_locations) >= cell_count:
                break
            index = random.randint(0, cell_count - 1)

            while index in pokemon_locations:
                index = random.randint(0, cell_count - 1)

            pokemon_locations += (index,)

        self._pokemon_locations = pokemon_locations

    def get_num_pokemon(self):
        """ Calculate how many pokemons in this game """
        return self._num_pokemon

    def check_win(self):
        """
        Checking if the player has won the game.
            Returns:
                True: if win the game
                False: if lose the game

        """

        return UNEXPOSED not in self._game_string and self._game_string.count(FLAG) == len(self._pokemon_locations)

    def flag_cell(self, index):
        """Toggle Flag on or off at selected index. If the selected index is already
            revealed, the game would return with no changes.

            Parameters:
                index (int): The index in the game string where a flag is placed.
            Returns
                (str): The updated game string.
        """

        if self._game_string[index] == FLAG:
            self._game_string = self.replace_character_at_index(index, UNEXPOSED)

        elif self._game_string[index] == UNEXPOSED:
            self._game_string = self.replace_character_at_index(index, FLAG)

    def reveal_cells(self, index):
        """
        Reveals all neighbouring cells at index and repeats for all
        cells that had a 0.

        Does not reveal flagged cells or cells with Pokemon.

        Parameters:
            index (int): Index of the currently selected cell

        Returns:
            (str): The updated game string
        """
        number = self.number_at_cell(index)

        game = self.replace_character_at_index(index, str(number))
        clear = self.big_fun_search(index)
        for i in clear:
            if game[i] != FLAG:
                number = self.number_at_cell(i)
                game = self.replace_character_at_index(i, str(number))

        self._game_string = game
        return self._game_string

    def replace_character_at_index(self, index, character):
        """
        A specified index in the game string at the specified index is replaced by
        a new character.

        Parameters:
            index (int): The index in the game string where the character is replaced.
            character (str): The new character that will be replacing the old character.

        Returns:
            (str): The updated game string.
        """

        self._game_string = self._game_string[:index] + character + self._game_string[index + 1:]

        return self._game_string

    def index_in_direction(self, index, direction):
        """
       This function takes in the index to a cell in the game string
    and returns a new index corresponding to an adjacent cell in the specified direction.

        Return None for invalid directions.

            Paramaters:
        index (int): the index of the action in the game string
        grid_size (int): size of game
        direction (str): specific direction to find the neighbor of the selected

            Returns:
        neighbor index (int): return the specific direction cell's index
        """

        if direction == UP:
            if index < self._grid_size:
                return
            return index - self._grid_size

        if direction == DOWN:
            if index > (self._grid_size ** 2 - self._grid_size) - 1:
                return
            return index + self._grid_size

        if direction == LEFT:
            if index % self._grid_size == 0:
                return
            return index - 1

        if direction == RIGHT:
            if (index + 1) % self._grid_size == 0:
                return
            return index + 1

        if direction == f"{UP}-{LEFT}":
            if index % self._grid_size == 0:
                return
            if index < self._grid_size:
                return
            return index - self._grid_size - 1

        if direction == f"{UP}-{RIGHT}":
            if (index + 1) % self._grid_size == 0:
                return
            if index < self._grid_size:
                return
            return index - self._grid_size + 1

        if direction == f"{DOWN}-{LEFT}":
            if index >= self._grid_size ** 2 - self._grid_size:
                return
            if index % self._grid_size == 0:
                return
            return index + self._grid_size - 1

        if direction == f"{DOWN}-{RIGHT}":
            if index > (self._grid_size ** 2 - self._grid_size) - 1:
                return
            if (index + 1) % self._grid_size == 0:
                return
            return index + self._grid_size + 1

    def index_to_position(self, index):
        """ Convert the game string index to the row, column coordinate.

        Parameters:
            index : the index of the cell in the game string

        Returns:
            tuple<int, int>: The row, column position of a cell
        """
        y = index // self._grid_size
        x = index % self._grid_size

        return x, y

    def position_to_index(self, position):
        """Convert the row, column coordinate in the grid to the game strings index.

        Parameters:
            position (tuple<int, int>): The row, column position of a cell.

        Returns:
            (int): The index of the cell in the game string.
        """

        x, y = position
        return y * self._grid_size + x

    def get_num_attempted_catches(self):
        """
        Calculate how many pokeballs are used currently

        Returns:
            (int): number of used pokeballs

        """

        used_pokeballs = 0
        game_string = self._game_string
        for cell in game_string:
            if cell == FLAG:
                used_pokeballs += 1
        return used_pokeballs

    def neighbour_directions(self, index):
        """
    #   This function returns a list of indexes that have a neighbouring cell.

    #   Paramaters:
        index (int): the index of the action in the game string.
        grid_size (int): Size of game.

    #   Returns:
        a list which contains all the indexes of neighbouring cell

        """

        neighbour1 = []

        if index > self._grid_size ** 2:
            return

        for direction in DIRECTIONS:
            neighbour1.append(self.index_in_direction(index, f"{UP}-{LEFT}"))
            neighbour1.append(self.index_in_direction(index, UP))
            neighbour1.append(self.index_in_direction(index, f"{UP}-{RIGHT}"))
            neighbour1.append(self.index_in_direction(index, LEFT))
            neighbour1.append(self.index_in_direction(index, RIGHT))
            neighbour1.append(self.index_in_direction(index, f"{DOWN}-{LEFT}"))
            neighbour1.append(self.index_in_direction(index, DOWN))
            neighbour1.append(self.index_in_direction(index, f"{DOWN}-{RIGHT}"))
            neighbour = [_ for _ in neighbour1 if _ != None]
            return neighbour

    def number_at_cell(self, index):
        """Calculates what number should be displayed at that specific index in the game.

        Parameters:
            index (int): Index of the currently selected cell

        Returns:
            (int): Number to be displayed at the given index in the game string.
    """
        if self._game_string[index] != UNEXPOSED:
            return int(self._game_string[index])

        number = 0
        for neighbour in self.neighbour_directions(index):
            if neighbour in self._pokemon_locations:
                number += 1

        return number

    def big_fun_search(self, index):
        """Searching adjacent cells to see if there are any Pokemon"s present.

        Using some sick algorithms.

        Find all cells which should be revealed when a cell is selected.

        For cells which have a zero value (i.e. no neighbouring pokemons) all the cell"s
        neighbours are revealed. If one of the neighbouring cells is also zero then
        all of that cell"s neighbours are also revealed. This repeats until no
        zero value neighbours exist.

        For cells which have a non-zero value (i.e. cells with neighbour pokemons), only
        the cell itself is revealed.

        Parameters:
            index (int): Index of the currently selected cell

        Returns:
            (list<int>): List of cells to turn visible.

        References:
            a1_solution(1).py
            https://learn.uq.edu.au/webapps/blackboard/content/listContent.jsp?course_id=_128547_1&content_id=_5017694_1
        """

        queue = [index]
        discovered = [index]
        visible = []

        if self._game_string[index] == FLAG:
            return queue

        number = self.number_at_cell(index)
        if number != 0:
            return queue

        while queue:
            node = queue.pop()
            for neighbour in self.neighbour_directions(node):
                if neighbour in discovered:
                    continue

                discovered.append(neighbour)
                if self._game_string[neighbour] != FLAG:
                    number = self.number_at_cell(neighbour)
                    if number == 0:
                        queue.append(neighbour)
                visible.append(neighbour)
        return visible


class BoardView(tk.Canvas):
    """View of the Pokemon game board"""

    def __init__(self, master, grid_size, board_width=600, *args, **kwargs):
        """Construct a board view from a game string.

           Parameters:
               master (tk.Widget): Widget within which the board is placed.
               grid_size (int): the size of the game.
               board_width (int): the size of the board
           """
        super().__init__(master, width=board_width, height=board_width, *args, **kwargs)
        self._master = master
        self._grid_size = grid_size
        self._board_width = board_width
        self._radius = (self._board_width / self._grid_size) / 2  # use for calculating the position
        self._length = self._radius * 2

    def draw_board(self, board):
        """ Draw the game board """

        self.delete(tk.ALL)
        for i in range(len(board)):
            x = i % self._grid_size
            y = i // self._grid_size
            if board[i] == UNEXPOSED:
                self.create_rectangle(x * self._length, y * self._length, self._length * (x + 1),
                                      self._length * (y + 1), fill='dark green')


            elif board[i] == FLAG:
                self.create_rectangle(x * self._length, y * self._length, self._length * (x + 1),
                                      self._length * (y + 1), fill='red')

            elif board[i] == POKEMON:
                self.create_rectangle(x * self._length, y * self._length, self._length * (x + 1),
                                      self._length * (y + 1), fill='yellow')

            else:
                self.create_rectangle(x * self._length, y * self._length, self._length * (x + 1),
                                      self._length * (y + 1), fill='light green')

                self.create_text(self._length * (x + 0.5), self._length * (y + 0.5), text=board[i])

    def get_bbox(self, pixel):
        """ Returns the bounding box for a cell centered at the provided pixel coordinates.

            Parameters:
                pixel (tuple<int,int>): the information of the click/motion on the canvas
        """
        bound_left_up = pixel[0] - self._radius, pixel[1] - self._radius
        bount_right_down = pixel[0] + self._radius, pixel[1] + self._radius
        return bound_left_up, bount_right_down

    def position_to_pixel(self, position):
        """ Returns the center pixel for the cell at position. """
        pixel_x = (position[0] * 2 + 1) * self._radius
        pixel_y = (position[1] * 2 + 1) * self._radius

        return pixel_x, pixel_y

    def pixel_to_position(self, pixel):
        """ Converts the supplied pixel to the position of the cell it is contained within. """
        position_x = int(pixel[0] // self._length)
        position_y = int(pixel[1] // self._length)

        return position_x, position_y

    def draw_motion(self, position):
        """ Draw the border when mouse move into the cell """

        input_position_x, input_position_y = self.pixel_to_position(position)
        input_pixel_x, input_pixel_y = self.position_to_pixel((input_position_x, input_position_y))
        up_bound, down_bound = self.get_bbox((input_pixel_x, input_pixel_y))

        self.create_line(up_bound, (up_bound[0] + self._length, up_bound[1]), width=3)
        self.create_line((up_bound[0] + self._length, up_bound[1]), down_bound, width=3)
        self.create_line(down_bound, (down_bound[0] - self._length, down_bound[1]), width=3)
        self.create_line((down_bound[0] - self._length, down_bound[1]), up_bound, width=3)


class ImageBoardView(BoardView):
    """ This class is inherit from BoardView, and It can shows the image when play the game"""

    def __init__(self, master, grid_size, board_width=600, *args, **kwargs):
        """Construct a board view from a game string.

           Parameters:
               master (tk.Widget): Widget within which the board is placed.
               grid_size (int): the size of the game.
               board_width (int): the size of the board
       """
        super().__init__(master, board_width)

        self._master = master
        self._board_width = board_width
        self._grid_size = grid_size
        self._radius = int((self._board_width / self._grid_size) / 2)
        self._length = int(self._radius * 2)

        long_glass = Image.open('images/unrevealed.gif')  # the unrevealed glass
        self.long_glass = long_glass.resize((self._length, self._length), Image.ANTIALIAS)
        self.long_glass = ImageTk.PhotoImage(self.long_glass)

        short_glass = Image.open('images/unrevealed_moved.gif')  # the unrevealed glass when mouse in it
        self.short_glass = short_glass.resize((self._length, self._length), Image.ANTIALIAS)
        self.short_glass = ImageTk.PhotoImage(self.short_glass)

        ball = Image.open('images/pokeball.gif')  # the pokeball when right click the cell
        self.ball = ball.resize((self._length, self._length), Image.ANTIALIAS)
        self.ball = ImageTk.PhotoImage(self.ball)

        def resize(name):
            """
            Use this function to resize the image size in order to fit the board size
            Args:
                name: the name of the image

            Returns:
                the resize image
            """
            name = name.resize((self._length, self._length), Image.ANTIALIAS)
            name = ImageTk.PhotoImage(name)
            return name

        self._pokemon_image = []  # a list that contains all the information about pokemon image
        pokemon1 = Image.open('images/pokemon_sprites/charizard.gif')
        pokemon1 = resize(pokemon1)

        pokemon2 = Image.open('images/pokemon_sprites/cyndaquil.gif')
        pokemon2 = resize(pokemon2)

        pokemon3 = Image.open('images/pokemon_sprites/pikachu.gif')
        pokemon3 = resize(pokemon3)

        pokemon4 = Image.open('images/pokemon_sprites/psyduck.gif')
        pokemon4 = resize(pokemon4)

        pokemon5 = Image.open('images/pokemon_sprites/togepi.gif')
        pokemon5 = resize(pokemon5)

        pokemon6 = Image.open('images/pokemon_sprites/umbreon.gif')
        pokemon6 = resize(pokemon6)

        self._pokemon_image.append(pokemon1)
        self._pokemon_image.append(pokemon2)
        self._pokemon_image.append(pokemon3)
        self._pokemon_image.append(pokemon4)
        self._pokemon_image.append(pokemon5)
        self._pokemon_image.append(pokemon6)

        self._number_at_cell = []  # a list that contains all the information about number image

        zero = Image.open('images/zero_adjacent.gif')
        zero = resize(zero)

        one = Image.open('images/one_adjacent.gif')
        one = resize(one)

        two = Image.open('images/two_adjacent.gif')
        two = resize(two)

        three = Image.open('images/three_adjacent.gif')
        three = resize(three)

        four = Image.open('images/four_adjacent.gif')
        four = resize(four)

        five = Image.open('images/five_adjacent.gif')
        five = resize(five)

        six = Image.open('images/six_adjacent.gif')
        six = resize(six)

        seven = Image.open('images/seven_adjacent.gif')
        seven = resize(seven)

        eight = Image.open('images/eight_adjacent.gif')
        eight = resize(eight)

        self._number_at_cell.append(zero)
        self._number_at_cell.append(one)
        self._number_at_cell.append(two)
        self._number_at_cell.append(three)
        self._number_at_cell.append(four)
        self._number_at_cell.append(five)
        self._number_at_cell.append(six)
        self._number_at_cell.append(seven)
        self._number_at_cell.append(eight)

    def draw_board(self, board):
        """
        Draw the image game board
        Args:
            board: the game string

        Returns:
            An image game board
        """
        self.delete(tk.ALL)
        for i in range(len(board)):
            x = i % self._grid_size
            y = i // self._grid_size
            if board[i] == UNEXPOSED:
                self.create_image(self._length * (x + 0.5), self._length * (y + 0.5), image=self.long_glass)

            elif board[i] == FLAG:
                self.create_image(self._length * (x + 0.5), self._length * (y + 0.5), image=self.ball)

            elif board[i] == POKEMON:
                self.create_image(self._length * (x + 0.5), self._length * (y + 0.5),
                                  image=random.choice(self._pokemon_image))

            else:
                self.create_image(self._length * (x + 0.5), self._length * (y + 0.5),
                                  image=self._number_at_cell[int(board[i])])

    def draw_motion1(self, position):
        """
         Motion on tall grass squares should cause the grass to ‘rustle’. Motion onto a tall grass square should cause
         the image to change to the ‘unexposed moved.png’ image, whereas motion off a tall grass square should restore
         the image to the ‘unexposed.png’ image.

        Args:
            position: the position for the mouse currently on

        Returns:
            A new image game board

        """
        input_position_x, input_position_y = self.pixel_to_position(position)
        input_pixel_x, input_pixel_y = self.position_to_pixel((input_position_x, input_position_y))
        self.create_image(input_pixel_x, input_pixel_y, image=self.short_glass)


class StatusBar(tk.Frame):
    """
    Include a game timer displaying the number of minutes and seconds the user has been playing the current game, as
    well as a representation of the number of current ‘attempted catches’, and the number of pokeballs the user has
    remaining.
    """

    def __init__(self, master):
        """Construct a status bar which contains some information about the game
        Args:
            master (tk.Widget): Widget within which the board is placed.
        """
        super().__init__(master)
        self._master = master

        left_part = tk.Frame(self._master)  # left part of the status bar
        ball_image = tk.PhotoImage(file='images/pokeball.gif')
        label_ball = tk.Label(left_part, image=ball_image)
        label_ball.image = ball_image
        label_ball.pack(side=tk.LEFT)
        self.attemped_catches = tk.Label(left_part, text='0 attemped catches')
        self.attemped_catches.pack(side=tk.TOP)
        self.remain_balls = tk.Label(left_part, text=' pokeballs left')
        self.remain_balls.pack(side=tk.BOTTOM)
        left_part.pack(side=tk.LEFT)

        middle_part = tk.Frame(self._master)  # middle part of the status bar
        clock_image = tk.PhotoImage(file='images/clock.gif')
        label_clock = tk.Label(middle_part, image=clock_image)
        label_clock.image = clock_image
        label_clock.pack(side=tk.LEFT)
        time_info = tk.Label(middle_part, text='Time elapsed')
        time_info.pack()
        self.clock = tk.Label(middle_part, text='0m 0s')
        self.clock.pack()
        middle_part.pack(side=tk.LEFT)

        def new_game():  # this function will be redefined in the PokemonGame part
            pass

        def restart_game():  # this function will be redefined in the PokemonGame part
            pass

        right_part = tk.Frame(self._master)  # right part of the status bar
        self.new_game_button = tk.Button(right_part, text='New Game', command=new_game)
        self.new_game_button.pack(side=tk.TOP, padx=10, pady=10)
        self.restart_game_button = tk.Button(right_part, text='Restart Game', command=restart_game)
        self.restart_game_button.pack(side=tk.BOTTOM, padx=10, pady=10)
        right_part.pack(side=tk.LEFT)


class PokemonGame(object):
    """Game application that manages communication between the board model, board view/image board view and status bar.
    """

    def __init__(self, master, grid_size=10, num_pokemon=8, task='TASK_ONE'):
        """Create a new game app within a master widget"""
        if grid_size > 10 or grid_size < 2:  # check whether the game is out of range
            messagebox.showwarning(title='Error', message='Grid size is out of range, please check')
            pass
        elif num_pokemon <= 0 or num_pokemon > grid_size ** 2:
            messagebox.showwarning(title='Error', message='Pokemon number is out of range, please check')
            pass

        else:  # Generate common variables
            self._task = task
            self._master = master
            self._master.title = ('Pokemon Catch Game')
            self._master.geometry("600x800")
            self._model = BoardModel(grid_size, num_pokemon)
            self._num_pokemon = num_pokemon
            self._grid_size = grid_size

            # create menu bar
            menubar = tk.Menu(self._master)
            self._master.config(menu=menubar)  # tell master what its menubar is

            # within the menu bar create the file menu
            filemenu = tk.Menu(menubar)
            menubar.add_cascade(label="File", menu=filemenu)
            filemenu.add_command(label='Save Game', command=self.save_game)
            filemenu.add_command(label='Load Game', command=self.load_game)
            filemenu.add_command(label='Restart Game', command=self.restart_game)
            filemenu.add_command(label='New Game', command=self.new_game)
            filemenu.add_command(label='High Scores', command=self.high_score)
            filemenu.add_command(label='Quit', command=self.quit_game)
            self._filename = None

            if self._task == 'TASK_ONE':  # task 1 and 2 individually
                self._view = BoardView(self._master, grid_size)
                self._view.draw_board(self._model._game_string)
                self._view.bind('<Button-1>', self._left_click1)
                self._view.bind('<Button-2>', self._right_click1)
                self._view.bind('<Button-3>', self._right_click1)
                self._view.bind('<Motion>', self.motion1)
                self._view.pack()
                self._grid_size = grid_size
                self.num_pokemon = num_pokemon

            if self._task == 'TASK_TWO':  # This is for task two
                self._view = ImageBoardView(self._master, grid_size)
                self._view.bind('<Button-1>', self._left_click1)
                self._view.bind('<Button-2>', self._right_click1)
                self._view.bind('<Button-3>', self._right_click1)
                self._view.bind('<Motion>', self.motion2)
                self._view.draw_board(self._model._game_string)
                self._view.pack()
                self._grid_size = grid_size
                self._num_pokemon = num_pokemon
                self._status = StatusBar(self._master)

                self._status.remain_balls.config(text="{0} pokeballs left".format(self._num_pokemon))
                self._status.new_game_button.config(command=self.new_game)

                self.current_time = time.time()

                def config():
                    """ Calculate the game time """
                    minute = int((time.time() - self.current_time) / 60)
                    seconds = int(time.time() - self.current_time - minute * 60)
                    self._status.clock.configure(text="{}m {}s".format(minute, seconds))
                    root.after(1000, config)
                    return minute, seconds

                self._status.clock.after(1000, config)
                self._status.restart_game_button.config(command=self.restart_game)
                self._status.pack(side=tk.TOP)

    def motion1(self, event):
        """ Use this in Task one when the mouse is moving"""
        if not self._model.check_win():
            event_x, event_y = event.x, event.y
            self._view.draw_board(self._model._game_string)
            self._view.draw_motion((event_x, event_y))

    def motion2(self, event):
        """ Use this in Task two when the mouse is moving"""
        if not self._model.check_win():
            x, y = event.x, event.y
            pixel = (x, y)
            position = self._view.pixel_to_position(pixel)
            index = self._model.position_to_index(position)
            if index > len(self._model._game_string):
                pass
            else:
                if self._model._game_string[index] == UNEXPOSED:
                    self._view.draw_board(self._model._game_string)
                    self._view.draw_motion1((x, y))

    def update_status(self):
        """ Update the pokeball and attempted catches information in the status bar"""
        if self._task == 'TASK_TWO':
            self._status.attemped_catches.config(
                text="{0} attempted catches".format(self._model._game_string.count(FLAG)))
            self._status.remain_balls.config(
                text="{0} pokeballs left".format(self._num_pokemon
                                                 - self._model._game_string.count(FLAG)))

    def save_game(self):
        """ Save the current game as a .txt file"""
        if self._filename is None:
            filename = filedialog.asksaveasfilename()
            if '.txt' in filename and len(filename) > 4:  # check whether the user use the correct file name format
                self._filename = filename
            else:
                reply = messagebox.askyesno(title='File Name Error',
                                            message="Please enter the correct format file name (end with '.txt')")
                if reply == messagebox.YES:
                    filename = filedialog.asksaveasfilename()
                    if '.txt' in filename and len(filename) > 4:
                        self._filename = filename
                if reply == messagebox.NO:
                    pass

        if self._filename:
            fd = open(self._filename, 'w')
            game_string = self._model._game_string
            pokemon_location = str(self._model._pokemon_locations)
            grid_size = str(self._grid_size)

            fd.write(game_string + '\n')
            fd.write(pokemon_location + '\n')
            fd.write(grid_size + '\n')
            fd.close()

    def load_game(self):
        """ Load the previous game from the computer"""
        try:
            filename = filedialog.askopenfilename()

            self._model._game_string = self.get_line_context(filename, 1)
            self._model._pokemon_locations = tuple(eval(self.get_line_context(filename, 2)))
            self._model._grid_size = int(self.get_line_context(filename, 3))
            self._num_pokemon = len(self._model._pokemon_locations)
            self.update_status()
            self._view.draw_board(self._model._game_string)
            self.current_time = time.time()

        except:  # if cannot find the file, then restart the game
            self.restart_game()

    def get_line_context(self, filename, line_number):
        """ Get the context of each line"""
        return linecache.getline(filename, line_number).strip()

    def restart_game(self):
        """ Restart the game, do not change pokemon locations"""
        self._view.draw_board(self._model.restart_game())
        self._num_pokemon = len(self._model._pokemon_locations)
        self.current_time = time.time()
        self.update_status()

    def new_game(self):
        """ New game, change pokemon locations"""
        self._model.get_pokemon_locations()
        self._view.draw_board(self._model.restart_game())
        self.current_time = time.time()
        self._num_pokemon = len(self._model._pokemon_locations)
        self.update_status()

    def high_score(self):
        """ record the high scores of users"""
        pass

    def quit_game(self):
        """ Quit the current game and back to desktop"""
        reply = messagebox.askquestion(type=messagebox.YESNO, title='Quit', message='Do you really want to quit?')
        if reply == messagebox.YES:
            quit()
        if reply == messagebox.NO:
            pass

    def draw_pokemon(self):
        """ Draw the pokemon when the game is loss"""
        for i in self._model._pokemon_locations:
            self._model.replace_character_at_index(i, POKEMON)
        self._view.draw_board(self._model._game_string)

    def play_game(self, index):
        """ Flag and un-Flag cell, and check whether the user is win. """
        if not self._model.check_win():
            if self._model._game_string[index] != FLAG:
                if index in self._model._pokemon_locations:
                    self.draw_pokemon()
                    self._master.update()
                    reply = messagebox.askquestion(type=messagebox.YESNO, title="Game Over",
                                                   message='You lose! Would you like to play it again?')

                    if reply == messagebox.YES:
                        self.new_game()

                    if reply == messagebox.NO:
                        quit()


                else:
                    self._model._game_string = self._model.reveal_cells(index)

                    self._view.draw_board(self._model._game_string)


        else:
            self.draw_pokemon()
            self._master.update()
            messagebox.showwarning(title='Game Over', message='You win!')
            quit()

    def _left_click1(self, event):
        """ Get x, y coordinates of click
            Convert x, y coordinates to position and then to index in the game
            Reveal the cell at index in BoardModel
            Sends new state to controller
            Update game view
        """
        if POKEMON not in self._model._game_string:
            x, y = event.x, event.y
            pixel = (x, y)
            position = self._view.pixel_to_position(pixel)
            index = self._model.position_to_index(position)
            self.play_game(index)
            self._master.update()
            if self._model.check_win():
                messagebox.askyesno(title='Game Over', message='You win!')
                quit()

    def draw_flag(self, index):
        """ Flag the cell when right click the mouse"""
        self._model.flag_cell(index)
        self._view.draw_board(self._model._game_string)
        self.update_status()
        self._master.update()

    def _right_click1(self, event):
        """ Get x, y coordinates of click
            Convert x, y coordinates to position and then to index in the game
            Flag the cell at index in BoardModel
            Sends new state to controller
            Update game view
        """
        if self._model.check_win() == False:
            x, y = event.x, event.y
            pixel = (x, y)
            position = self._view.pixel_to_position(pixel)
            index = self._model.position_to_index(position)

            if self._model._game_string[index] != FLAG and self._model._game_string.count(FLAG) < self._num_pokemon:
                self.draw_flag(index)

            elif self._model._game_string[index] == FLAG:
                self.draw_flag(index)

            else:
                messagebox.askyesno(title='Warning', message='You do not have extra balls')

            if self._model.check_win():
                messagebox.askyesno(title='Game Over', message='You win!')
                quit()


root = tk.Tk()
root.title('Pokemon Games')

label = tk.Label(root, text='Pokemon: Got 2 Find Them All!', font=('Tahoma', 40), width=70, height=2, fg='white',
                 bg='#d26d6a')
label.pack(side=tk.TOP)

# Please input 'TASK_ONE' when checking function about task one, input 'TASK_TWO' when checking function about task two
PokemonGame(root, 10, 15, 'TASK_ONE')  # PokemonGame(root, grid_size, num_pokemon, task)


root.mainloop()
