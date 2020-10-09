import tkinter as tk
import random
from tkinter import messagebox
import time
import linecache
from tkinter import filedialog

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
EXPOSED = "0"


class BoardModel(object):
    def __init__(self, grid_size, num_pokemon):
        self._grid_size = grid_size

        self._num_pokemon = num_pokemon
        self._game_string = None
        self._pokemon_locations = None
        self.get_game()
        self.get_pokemon_locations()

    def get_game(self):
        game_string = UNEXPOSED * self._grid_size ** 2

        self._game_string = game_string
        return self._game_string

    def restart_game(self):
        return self.get_game()

    def new_game(self):
        return self.get_pokemon_locations()

    def get_pokemon_locations(self):
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
        return self._num_pokemon

    def check_win(self):
        """Checking if the player has won the game.

        Parameters:
            game (str): Game string.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.

        Returns:
            (bool): True if the player has won the game, false if not.

        """

        return UNEXPOSED not in self._game_string and self._game_string.count(FLAG) == len(self._pokemon_locations)

    def flag_cell(self, index):
        """Toggle Flag on or off at selected index. If the selected index is already
            revealed, the game would return with no changes.

            Parameters:
                game (str): The game string.
                index (int): The index in the game string where a flag is placed.
            Returns
                (str): The updated game string.
        """

        if self._game_string[index] == FLAG:
            self._game_string = self.replace_character_at_index(index, UNEXPOSED)

        elif self._game_string[index] == UNEXPOSED:
            self._game_string = self.replace_character_at_index(index, FLAG)

    def reveal_cells(self, index):
        """Reveals all neighbouring cells at index and repeats for all
        cells that had a 0.

        Does not reveal flagged cells or cells with Pokemon.

        Parameters:
            game (str): Game string.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            grid_size (int): Size of game.
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
        """A specified index in the game string at the specified index is replaced by
        a new character.
        Parameters:
            game (str): The game string.
            index (int): The index in the game string where the character is replaced.
            character (str): The new character that will be replacing the old character.

        Returns:
            (str): The updated game string.
        """

        self._game_string = self._game_string[:index] + character + self._game_string[index + 1:]

        return self._game_string

    def index_in_direction(self, index, direction):
        """
    #   This function takes in the index to a cell in the game string
    and returns a new index corresponding to an adjacent cell in the specified direction.

    #   Return None for invalid directions.

    #   Paramaters:
        index (int): the index of the action in the game string
        grid_size (int): size of game
        direction (str): specific direction to find the neighbor of the selected

        #   Returns:
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
        y = index // self._grid_size
        x = index % self._grid_size

        return x, y

    def position_to_index(self, position):
        x, y = position
        return y * self._grid_size + x

    def get_num_attempted_catches(self):

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
            game (str): Game string.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            grid_size (int): Size of game.
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

    def __init__(self, master, grid_size, board_width=600, *args, **kwargs):
        super().__init__(master, width=600, height=600, *args, **kwargs)
        self._master = master
        self._grid_size = grid_size
        self._board_width = board_width
        self._radius = (self._board_width / self._grid_size) / 2
        self._length = self._radius * 2

    def draw_board(self, board):  # board是Model里的game string
        # ~~~~121~~~~~~

        self.delete(tk.ALL)
        for i in range(len(board)):
            x = i % self._grid_size
            y = i // self._grid_size
            if board[i] == UNEXPOSED:
                self.create_rectangle(x * 60, y * 60, 60 * (x + 1), 60 * (y + 1), fill='dark green')
                # self.create_text(60 * (x+ 0.5), 60 * (y + 0.5), text=board[i])

            elif board[i] == FLAG:
                self.create_rectangle(x * 60, y * 60, 60 * (x + 1), 60 * (y + 1), fill='red')

            elif board[i] == POKEMON:
                self.create_rectangle(x * 60, y * 60, 60 * (x + 1), 60 * (y + 1), fill='yellow')

            else:
                self.create_rectangle(x * 60, y * 60, 60 * (x + 1), 60 * (y + 1), fill='light green')
                self.create_text(60 * (x + 0.5), 60 * (y + 0.5), text=board[i])

    def get_bbox(self, pixel):

        bound_left_up = pixel[0] - self._radius, pixel[1] - self._radius
        bount_right_down = pixel[0] + self._radius, pixel[1] + self._radius
        return bound_left_up, bount_right_down

    def position_to_pixel(self, position):
        pixel_x = (position[0] * 2 + 1) * self._radius
        pixel_y = (position[1] * 2 + 1) * self._radius

        return pixel_x, pixel_y

    def pixel_to_position(self, pixel):
        position_x = int(pixel[0] // self._length)
        position_y = int(pixel[1] // self._length)

        return position_x, position_y

    def draw_motion(self, position):

        input_position_x, input_position_y = self.pixel_to_position(position)
        input_pixel_x, input_pixel_y = self.position_to_pixel((input_position_x, input_position_y))
        up_bound, down_bound = self.get_bbox((input_pixel_x, input_pixel_y))
        # self.create_rectangle(up_bound, down_bound,fill='dark green')
        self.create_line(up_bound, (up_bound[0] + self._length, up_bound[1]), width=3)
        self.create_line((up_bound[0] + self._length, up_bound[1]), down_bound, width=3)
        self.create_line(down_bound, (down_bound[0] - self._length, down_bound[1]), width=3)
        self.create_line((down_bound[0] - self._length, down_bound[1]), up_bound, width=3)


class StatusBar(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._master = master
        left_part = tk.Frame(self._master)
        ball_image = tk.PhotoImage(file='images/pokeball.gif')
        label_ball = tk.Label(left_part, image=ball_image)
        label_ball.image = ball_image
        label_ball.pack(side=tk.LEFT)
        self.attemped_catches = tk.Label(left_part, text='0 attemped catches')
        self.attemped_catches.pack(side=tk.TOP)
        self.remain_balls = tk.Label(left_part, text=' pokeballs left')
        self.remain_balls.pack(side=tk.BOTTOM)
        left_part.pack(side=tk.LEFT)

        middle_part = tk.Frame(self._master)
        clock_image = tk.PhotoImage(file='images/clock.gif')
        label_clock = tk.Label(middle_part, image=clock_image)
        label_clock.image = clock_image
        label_clock.pack(side=tk.LEFT)
        time_info = tk.Label(middle_part, text='Time elapsed')
        time_info.pack()
        self.clock = tk.Label(middle_part, text='0m 0s')
        self.clock.pack()

        middle_part.pack(side=tk.LEFT)

        def new_game():
            pass

        def restart_game():
            pass

        right_part = tk.Frame(self._master)
        self.new_game_button = tk.Button(right_part, text='New Game', command=new_game)
        self.new_game_button.pack(side=tk.TOP, padx=10, pady=10)
        self.restart_game_button = tk.Button(right_part, text='Restart Game', command=restart_game)
        self.restart_game_button.pack(side=tk.BOTTOM, padx=10, pady=10)
        right_part.pack(side=tk.LEFT)

    # def update(self):


class ImageBoardView(BoardView):
    def __init__(self, master, grid_size, board_width=600):
        super().__init__(master, board_width)
        self._master = master
        self._grid_size = grid_size
        self._board_width = board_width
        self._radius = (self._board_width / self._grid_size) / 2
        self._length = self._radius * 2

        self.long_glass = tk.PhotoImage(file='images/unrevealed.gif')
        self.short_glass = tk.PhotoImage(file='images/unrevealed_moved.gif')
        self.ball = tk.PhotoImage(file='images/pokeball.gif')

        self._pokemons = []
        pokemon1 = tk.PhotoImage(file='images/pokemon_sprites/charizard.gif')
        pokemon2 = tk.PhotoImage(file='images/pokemon_sprites/cyndaquil.gif')
        pokemom3 = tk.PhotoImage(file='images/pokemon_sprites/pikachu.gif')
        pokemon4 = tk.PhotoImage(file='images/pokemon_sprites/psyduck.gif')
        pokemon5 = tk.PhotoImage(file='images/pokemon_sprites/togepi.gif')
        pokemon6 = tk.PhotoImage(file='images/pokemon_sprites/umbreon.gif')
        self._pokemons.append(pokemon1)
        self._pokemons.append(pokemon2)
        self._pokemons.append(pokemom3)
        self._pokemons.append(pokemon4)
        self._pokemons.append(pokemon5)
        self._pokemons.append(pokemon6)

        self._number_at_cell = []
        zero = tk.PhotoImage(file='images/zero_adjacent.gif')
        one = tk.PhotoImage(file='images/one_adjacent.gif')
        two = tk.PhotoImage(file='images/two_adjacent.gif')
        three = tk.PhotoImage(file='images/three_adjacent.gif')
        four = tk.PhotoImage(file='images/four_adjacent.gif')
        five = tk.PhotoImage(file='images/five_adjacent.gif')
        six = tk.PhotoImage(file='images/six_adjacent.gif')
        seven = tk.PhotoImage(file='images/seven_adjacent.gif')
        eight = tk.PhotoImage(file='images/eight_adjacent.gif')
        self._number_at_cell.append(zero)
        self._number_at_cell.append(one)
        self._number_at_cell.append(two)
        self._number_at_cell.append(three)
        self._number_at_cell.append(four)
        self._number_at_cell.append(five)
        self._number_at_cell.append(six)
        self._number_at_cell.append(seven)
        self._number_at_cell.append(eight)

    def draw_board(self, board):  # board是Model里的game string

        self.delete(tk.ALL)
        for i in range(len(board)):
            x = i % self._grid_size
            y = i // self._grid_size
            if board[i] == UNEXPOSED:
                self.create_image((2 * x + 1) * 30, (2 * y + 1) * 30, image=self.long_glass)
                # self.create_text(60 * (x+ 0.5), 60 * (y + 0.5), text=board[i])

            elif board[i] == FLAG:
                self.create_image((2 * x + 1) * 30, (2 * y + 1) * 30, image=self.ball)

            elif board[i] == POKEMON:
                self.create_image((2 * x + 1) * 30, (2 * y + 1) * 30, image=random.choice(self._pokemons))

            else:
                self.create_image((2 * x + 1) * 30, (2 * y + 1) * 30, image=self._number_at_cell[int(board[i])])

    def draw_motion1(self, position):

        input_position_x, input_position_y = self.pixel_to_position(position)
        input_pixel_x, input_pixel_y = self.position_to_pixel((input_position_x, input_position_y))
        self.create_image(input_pixel_x, input_pixel_y, image=self.short_glass)


class PokemonGame(object):
    def __init__(self, master, grid_size=10, num_pokemon=8, task='TASK_ONE'):
        if grid_size > 10 or grid_size < 2:
            pass

        elif num_pokemon < 0 or num_pokemon > grid_size ** 2:
            pass

        else:
            self._task = task
            self._master = master
            self._master.title = ('Pokemon Game')
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
            # self._game_string = self._model._game_string

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

            if self._task == 'TASK_TWO':
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
                    minute = int((time.time() - self.current_time) / 60)
                    seconds = int(time.time() - self.current_time - minute * 60)
                    self._status.clock.configure(text="{}m {}s".format(minute, seconds))
                    root.after(1000, config)
                    return minute, seconds

                self._status.clock.after(1000, config)
                self._status.restart_game_button.config(command=self.restart_game)
                self._status.pack()

    def motion1(self, event):
        if self._model.check_win() == False:
            event_x, event_y = event.x, event.y
            self._view.draw_board(self._model._game_string)
            self._view.draw_motion((event_x, event_y))

    def motion2(self, event):
        if self._model.check_win() == False:
            x, y = event.x, event.y
            pixel = (x, y)
            position = self._view.pixel_to_position(pixel)
            index = self._model.position_to_index(position)
            if self._model._game_string[index] == UNEXPOSED:
                self._view.draw_board(self._model._game_string)
                self._view.draw_motion1((x, y))

    def update_status(self):
        if self._task == 'TASK_TWO':
            self._status.attemped_catches.config(
                text="{0} attemped catches".format(self._model._game_string.count(FLAG)))
            self._status.remain_balls.config(
                text="{0} pokeballs left".format(self._num_pokemon
                                                 - self._model._game_string.count(FLAG)))

    def save_game(self):
        if self._filename is None:
            filename = filedialog.asksaveasfilename()
            if '.txt' in filename and len(filename) > 4:
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
            # self._master.title(self._filename)
            fd = open(self._filename, 'w')
            game_string = self._model._game_string
            pokemon_location = str(self._model._pokemon_locations)
            grid_size = str(self._grid_size)

            fd.write(game_string + '\n')
            fd.write(pokemon_location + '\n')
            fd.write(grid_size + '\n')
            fd.close()

    def load_game(self):

        try:
            filename = filedialog.askopenfilename()

            self._model._game_string = self.get_line_context(filename, 1)
            self._model._pokemon_locations = tuple(eval(self.get_line_context(filename, 2)))
            self._model._grid_size = int(self.get_line_context(filename, 3))
            self._num_pokemon = len(self._model._pokemon_locations)
            self.update_status()
            self._view.draw_board(self._model._game_string)
            self.current_time = time.time()
        except:
            self.restart_game()

    def get_line_context(self, filename, line_number):
        return linecache.getline(filename, line_number).strip()

    def restart_game(self):
        self._view.draw_board(self._model.restart_game())
        self._num_pokemon = len(self._model._pokemon_locations)
        self.current_time = time.time()
        self.update_status()

    def new_game(self):
        self._model.get_pokemon_locations()
        self._view.draw_board(self._model.restart_game())
        self.current_time = time.time()
        self._num_pokemon = len(self._model._pokemon_locations)
        self.update_status()

    def high_score(self):
        pass

    def quit_game(self):
        reply = messagebox.askquestion(type=messagebox.YESNO, title='Quit', message='Do you really want to quit?')
        if reply == messagebox.YES:
            quit()
        if reply == messagebox.NO:
            pass

    def draw_pokemon(self):
        for i in self._model._pokemon_locations:
            self._model.replace_character_at_index(i, POKEMON)
        self._view.draw_board(self._model._game_string)

    def play_game(self, index):
        if self._model.check_win() == False:
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
        if POKEMON not in self._model._game_string:
            x, y = event.x, event.y
            pixel = (x, y)
            position = self._view.pixel_to_position(pixel)
            index = self._model.position_to_index(position)
            self.play_game(index)

        # get x, y coordinates of click
        # convert x, y coordinates to position and then to index in the game
        # reveal the cell at index in model
        # sends new state to controller (i.e. model.get_game())
        # update view (view.draw_board)

    def draw_flag(self, index):
        self._model.flag_cell(index)
        self._view.draw_board(self._model._game_string)
        self.update_status()
        self._master.update()

    def _right_click1(self, event):
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

label = tk.Label(root, text='Pokemon: Got 2 Find Them All!', width=60, height=5, bg='pink')
label.pack(side=tk.TOP)
PokemonGame(root, 10, 4, 'TASK_TWO')

root.mainloop()
