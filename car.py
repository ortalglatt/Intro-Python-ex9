class Car:
    """
    Class of Car objects, contains the name of the car, the length, the
    location and the orientation.
    This class contains functions that return an information about the car, and
    functions that change the car attribute if needed.
    """
    ROW = 0
    COL = 1
    VERTICAL = 0
    HORIZONTAL = 1
    RIGHT, LEFT, UP, DOWN = "r", "l", "u", "d"
    R_MSG = "cause the car to move one step to the right"
    L_MSG = "cause the car to move one step to the left"
    D_MSG = "cause the car to move one step down"
    U_MSG = "cause the car to move one step up"

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col)
        location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        :return: None
        """
        self.__name = name
        self.__length = length
        self.__location = location
        self.__orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        row, col = self.__location[self.ROW], self.__location[self.COL]
        car_coordinates = []
        if self.__orientation == self.VERTICAL:
            for i in range(row, row + self.__length):
                car_coordinates.append((i, col))
        elif self.__orientation == self.HORIZONTAL:
            for i in range(col, col + self.__length):
                car_coordinates.append((row, i))
        return car_coordinates

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements
        permitted by this car.
        """
        possible_movements = {}
        if self.__orientation == self.HORIZONTAL:
            possible_movements[self.RIGHT] = self.R_MSG
            possible_movements[self.LEFT] = self.L_MSG
        elif self.__orientation == self.VERTICAL:
            possible_movements[self.DOWN] = self.D_MSG
            possible_movements[self.UP] = self.U_MSG
        return possible_movements

    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this
        move to be legal.
        """
        car_coor = Car.car_coordinates(self)
        row, col = self.__location[self.ROW], self.__location[self.COL]
        if movekey == self.RIGHT:
            return [(row, car_coor[-1][self.COL] + 1)]
        elif movekey == self.LEFT:
            return [(row, col - 1)]
        elif movekey == self.DOWN:
            return [(car_coor[-1][self.ROW] + 1, col)]
        elif movekey == self.UP:
            return [(row - 1, col)]

    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        possible_moves = Car.possible_moves(self)
        if movekey in possible_moves:
            row, col = self.__location[self.ROW], self.__location[self.COL]
            if movekey == self.RIGHT:
                self.__location = (row, col + 1)
            elif movekey == self.LEFT:
                self.__location = (row, col - 1)
            elif movekey == self.DOWN:
                self.__location = (row + 1, col)
            elif movekey == self.UP:
                self.__location = (row - 1, col)
            return True
        return False

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.__name
