class Board:
    """
    Class of Board objects.
    This class contains function the print the board, functions that change the
    board of needed, and functions that return information about the board.
    return an information about the car, and
    """
    ROW = 0
    COL = 1
    SIZE = 7
    TARGET = (3, 7)
    BEF_TAR = (3, 6)
    EMPTY = '_'
    EXIT = "->"
    STAR = '*'
    FIRST = 0
    LAST = 6
    RIGHT, LEFT, UP, DOWN = "r", "l", "u", "d"

    def __init__(self):
        """
        Initialize a new Board object.
        :return: None
        """
        self.__board = []
        for row in range(self.SIZE):
            new_row = [self.EMPTY for col in range(self.SIZE)]
            if row == 3:
                new_row.append(self.EXIT)
            else:
                new_row.append(self.STAR)
            self.__board.append(new_row)
        self.__cars = {}

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        string_to_print = ""
        for row in self.__board:
            string_to_print += " ".join(row) + "\n"
        return string_to_print

    def cell_list(self):
        """
        This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        coor_list = []
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                coor_list.append((row, col))
        coor_list.append(self.TARGET)
        return coor_list

    def possible_moves(self):
        """
        This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """
        legal_move_list = []
        for car_name, car in self.__cars.items():
            possible_moves = self.__possible_moves_helper(car)
            for move in possible_moves:
                cell_to_move = car.movement_requirements(move)[0]
                if not self.cell_content(cell_to_move):
                    legal_move_list.append((car_name, move,
                                            possible_moves[move]))
        return legal_move_list

    def __possible_moves_helper(self, car):
        """
        Check in what directions the car can move, by considering the boarders
        of the board.
        :param car: the car object we want to check
        :return: dictionary of all the directions this car can move and their
        description
        """
        possible_moves = car.possible_moves()
        car_coor = car.car_coordinates()
        possible_movements = {}
        if self.RIGHT in possible_moves:
            if car_coor[-1] == self.BEF_TAR or \
                    car_coor[-1][self.COL] < self.LAST:
                possible_movements[self.RIGHT] = possible_moves[self.RIGHT]
            if car_coor[0][self.COL] > self.FIRST:
                possible_movements[self.LEFT] = possible_moves[self.LEFT]
        elif self.UP in possible_moves:
            if car_coor[-1][self.ROW] < self.LAST:
                possible_movements[self.DOWN] = possible_moves[self.DOWN]
            if car_coor[0][self.ROW] > self.FIRST:
                possible_movements[self.UP] = possible_moves[self.UP]
        return possible_movements

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be
        filled for victory.
        :return: (row,col) of goal location
        """
        return self.TARGET

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row, col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        row, col = coordinate[self.ROW], coordinate[self.COL]
        if self.__board[row][col] == self.EMPTY or \
                self.__board[row][col] == self.EXIT:
            return None
        return self.__board[row][col]

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        car_coor = car.car_coordinates()
        if not self.__check_if_car_valid(car_coor):
            return False
        self.__cars[car.get_name()] = car
        for coor in car_coor:
            self.__board[coor[self.ROW]][coor[self.COL]] = car.get_name()
        return True

    def __check_if_car_valid(self, car_coor):
        """
        Check if it's legal to put the car on the board.
        :param car_coor: a list of tuples of the car coordinates
        :return: True if it's legal to put the car on this coordinates, and
        False if it's not legal.
        """
        for coor in car_coor:
            row, col = coor[self.ROW], coor[self.COL]
            cell = (row, col)
            if row < self.FIRST or row > self.LAST or col < self.FIRST or \
                    col > self.LAST:
                return False
            elif self.cell_content(cell):
                return False
        return True

    def move_car(self, name, movekey):
        """
        Moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        for tup in self.possible_moves():
            if tup[0] == name and tup[1] == movekey:
                self.__move_car_helper(name, movekey)
                return True
        return False

    def __move_car_helper(self, name, movekey):
        """
        Moves the car to the direction you want, change the board and in the
        cars attributes.
        :param name: name of car you want to move
        :param movekey: key of the direction you want to move the car
        :return: None
        """
        car = self.__cars[name]
        coor_bef = car.car_coordinates()
        car.move(movekey)
        coor_af = car.car_coordinates()
        if movekey in [self.RIGHT, self.DOWN]:
            self.__board[coor_bef[0][self.ROW]][coor_bef[0][self.COL]] \
                = self.EMPTY
            self.__board[coor_af[-1][self.ROW]][coor_af[-1][self.COL]] = name
        elif movekey in [self.LEFT, self.UP]:
            self.__board[coor_af[0][self.ROW]][coor_af[0][self.COL]] = name
            self.__board[coor_bef[-1][self.ROW]][coor_bef[-1][self.COL]] = \
                self.EMPTY
