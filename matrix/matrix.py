from __future__ import annotations

from abc import ABC, abstractmethod

import pygame

try:
    from _types import *
except ImportError:
    from ._types import *


class Matrix(ABC):
    __subclasses: Dict[DimLike, Matrix] = {}

    # noinspection PyMethodOverriding, PyTypeChecker
    def __init_subclass__(cls, /, dimensions: DimLike, **kwargs) -> None:
        super().__init_subclass__()
        cls.__subclasses[dimensions] = cls

    def __new__(cls, array: MatrixLike) -> Matrix:
        if not (isinstance(array, list) and len(array)):
            raise TypeError("Input array needs to be a 2D array of floats")

        for row in array:
            if not (isinstance(row, list) and len(row)):
                raise TypeError("Input array needs to be a 2D array of floats")

            for elem in row:
                if not isinstance(elem, (float, int)):
                    raise TypeError("Input array needs to be a 2D array of floats")

        dimensions = (len(array), len(array[0]))

        if dimensions not in cls.__subclasses:
            raise ValueError("Invalid Dimensionality")

        # noinspection SpellCheckingInspection
        subcls = cls.__subclasses[dimensions]
        # noinspection PyTypeChecker
        return object.__new__(subcls)

    def __init__(self, array: MatrixLike) -> None:
        self._arr = array

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Matrix):
            return False
        return self._arr == other._arr

    def __neq__(self, other: Any) -> bool:
        return not self == other

    def __truediv__(self, other: Numeric) -> Matrix:
        is_number = isinstance(other, float) or isinstance(other, int)
        if not is_number:
            raise TypeError("cannot divide matrix by anything but a number")

        if other == 0:
            raise ZeroDivisionError("Cannot divide by zero")

        return (1 / other) * self  # needs __rmul__

    def transpose(self) -> Matrix:  # maybe another syntax will be convenient
        return Matrix([[self._arr[j][i] for j in range(len(self._arr))] for i in range(len(self._arr[0]))])

    def __sub__(self, other: Matrix) -> Matrix:  # self - other
        return self + (-1) * other  # needs __rmul__ and __add__

    @abstractmethod
    def __add__(self, other: Matrix) -> Matrix:  # self + other
        pass

    @abstractmethod
    def __mul__(self, other: pygame.Vector2 | Matrix | Numeric) -> pygame.Vector2 | Matrix:  # self * other
        pass

    @abstractmethod
    def __rmul__(self, other: Numeric) -> Matrix:  # other * self
        pass

    @abstractmethod
    def __abs__(self) -> float:  # determinant
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def inverse(self) -> Matrix:  # should probably also enable self ^ (-1) to call inverse
        pass


class Matrix22(Matrix, dimensions=(2, 2)):
    def __init__(self, array: MatrixLike) -> None:
        if len(array) != 2:
            raise ValueError("Array needs to have 2 rows")
        if len(array[0]) != 2 or len(array[1]) != 2:
            raise ValueError("Array needs to have 2 columns")

        super().__init__(array)

    def __add__(self, other: Matrix22) -> Matrix22:
        if not isinstance(other, Matrix22):
            raise TypeError("Can only add Matrix22 to Matrix22")

        x = self._arr
        y = other._arr
        x11 = x[0][0] + y[0][0]
        x12 = x[0][1] + y[0][1]
        x21 = x[1][0] + y[1][0]
        x22 = x[1][1] + y[1][1]

        return Matrix22([[x11, x12], [x21, x22]])

    def __mul__(self, other: pygame.Vector2 | TwoTall | Numeric) -> pygame.Vector2 | TwoTall:  # self * other
        if isinstance(other, pygame.Vector2):
            x = self._arr[0][0] * other.x + self._arr[0][1] * other.y
            y = self._arr[1][0] * other.x + self._arr[1][1] * other.y
            return pygame.Vector2(x, y)

        if isinstance(other, Numeric):
            arr = [[other * self._arr[j][i] for i in range(2)] for j in range(2)]
            return Matrix22(arr)

        if isinstance(other, Matrix22):
            x11 = self._arr[0][0] * other._arr[0][0] + self._arr[0][1] * other._arr[1][0]
            x12 = self._arr[0][0] * other._arr[0][1] + self._arr[0][1] * other._arr[1][1]
            x21 = self._arr[1][0] * other._arr[0][0] + self._arr[1][1] * other._arr[1][0]
            x22 = self._arr[1][0] * other._arr[0][1] + self._arr[1][1] * other._arr[1][1]

            return Matrix22([[x11, x12], [x21, x22]])

        if isinstance(other, Matrix23):
            x11 = self._arr[0][0] * other._arr[0][0] + self._arr[0][1] * other._arr[1][0]
            x12 = self._arr[0][0] * other._arr[0][1] + self._arr[0][1] * other._arr[1][1]
            x13 = self._arr[0][0] * other._arr[0][2] + self._arr[0][1] * other._arr[1][2]
            x21 = self._arr[1][0] * other._arr[0][0] + self._arr[1][1] * other._arr[1][0]
            x22 = self._arr[1][0] * other._arr[0][1] + self._arr[1][1] * other._arr[1][1]
            x23 = self._arr[1][0] * other._arr[0][2] + self._arr[1][1] * other._arr[1][2]

            return Matrix23([[x11, x12, x13], [x21, x22, x23]])

        if isinstance(other, Matrix24):
            x11 = self._arr[0][0] * other._arr[0][0] + self._arr[0][1] * other._arr[1][0]
            x12 = self._arr[0][0] * other._arr[0][1] + self._arr[0][1] * other._arr[1][1]
            x13 = self._arr[0][0] * other._arr[0][2] + self._arr[0][1] * other._arr[1][2]
            x14 = self._arr[0][0] * other._arr[0][3] + self._arr[0][1] * other._arr[1][3]
            x21 = self._arr[1][0] * other._arr[0][0] + self._arr[1][1] * other._arr[1][0]
            x22 = self._arr[1][0] * other._arr[0][1] + self._arr[1][1] * other._arr[1][1]
            x23 = self._arr[1][0] * other._arr[0][2] + self._arr[1][1] * other._arr[1][2]
            x24 = self._arr[1][0] * other._arr[0][3] + self._arr[1][1] * other._arr[1][3]

            return Matrix24([[x11, x12, x13, x14], [x21, x22, x23, x24]])

        raise TypeError(f"cannot multiply Matrix22 on the right by {type(other)}")

    def __rmul__(self, other: Numeric) -> Matrix22:  # other * self
        if not isinstance(other, Numeric):
            raise TypeError("cannot multiply matrix on the left by anything but a number")

        arr = [[other * self._arr[j][i] for i in range(2)] for j in range(2)]
        return Matrix22(arr)

    def __abs__(self) -> float:  # determinant
        return self._arr[0][0] * self._arr[1][1] - self._arr[0][1] * self._arr[1][0]

    def __str__(self) -> str:
        x = self._arr
        return f"{type(self).__name__}\n\t\t{x[0][0]}\t{x[0][1]}\n\t\t{x[1][0]}\t{x[1][1]}"

    def inverse(self) -> Matrix:  # should probably also enable self ^ (-1) to call inverse
        pass


class Matrix23(Matrix, dimensions=(2, 3)):
    def __init__(self, array: MatrixLike) -> None:
        if len(array) != 2:
            raise ValueError("Array needs to have 2 rows")
        if len(array[0]) != 3 or len(array[1]) != 3:
            raise ValueError("Array needs to have 3 columns")

        super().__init__(array)

    def __add__(self, other: Matrix23) -> Matrix23:
        if not isinstance(other, Matrix23):
            raise TypeError("Can only add Matrix23 to Matrix23")

        x = self._arr
        y = other._arr
        x11 = x[0][0] + y[0][0]
        x12 = x[0][1] + y[0][1]
        x13 = x[0][2] + y[0][2]
        x21 = x[1][0] + y[1][0]
        x22 = x[1][1] + y[1][1]
        x13 = x[1][2] + y[1][2]

        return Matrix23([[x11, x12, x13], [x21, x22, x23]])

    def __mul__(self, other: pygame.Vector3 | ThreeTall | Numeric) -> pygame.Vector2 | TwoTall:  # self * other
        if isinstance(other, pygame.Vector3):
            x = self._arr[0][0] * other.x + self._arr[0][1] * other.y + self._arr[0][2] * other.z
            y = self._arr[1][0] * other.x + self._arr[1][1] * other.y + self._arr[1][2] * other.z
            return pygame.Vector2(x, y)

        if isinstance(other, Numeric):
            arr = [[other * self._arr[j][i] for i in range(3)] for j in range(2)]
            return Matrix22(arr)

        if isinstance(other, Matrix32):
            x11 = self._arr[0][0] * other._arr[0][0] + self._arr[0][1] * other._arr[1][0] + self._arr[0][2] * other._arr[2][0]
            x12 = self._arr[0][0] * other._arr[0][1] + self._arr[0][1] * other._arr[1][1] + self._arr[0][2] * other._arr[2][1]
            x21 = self._arr[1][0] * other._arr[0][0] + self._arr[1][1] * other._arr[1][0] + self._arr[1][2] * other._arr[2][0]
            x22 = self._arr[1][0] * other._arr[0][1] + self._arr[1][1] * other._arr[1][1] + self._arr[1][2] * other._arr[2][1]

            return Matrix22([[x11, x12], [x21, x22]])

        if isinstance(other, Matrix23):  # need to do
            x11 = self._arr[0][0] * other._arr[0][0] + self._arr[0][1] * other._arr[1][0]
            x12 = self._arr[0][0] * other._arr[0][1] + self._arr[0][1] * other._arr[1][1]
            x13 = self._arr[0][0] * other._arr[0][2] + self._arr[0][1] * other._arr[1][2]
            x21 = self._arr[1][0] * other._arr[0][0] + self._arr[1][1] * other._arr[1][0]
            x22 = self._arr[1][0] * other._arr[0][1] + self._arr[1][1] * other._arr[1][1]
            x23 = self._arr[1][0] * other._arr[0][2] + self._arr[1][1] * other._arr[1][2]

            return Matrix23([[x11, x12, x13], [x21, x22, x23]])

        if isinstance(other, Matrix24):
            x11 = self._arr[0][0] * other._arr[0][0] + self._arr[0][1] * other._arr[1][0]
            x12 = self._arr[0][0] * other._arr[0][1] + self._arr[0][1] * other._arr[1][1]
            x13 = self._arr[0][0] * other._arr[0][2] + self._arr[0][1] * other._arr[1][2]
            x14 = self._arr[0][0] * other._arr[0][3] + self._arr[0][1] * other._arr[1][3]
            x21 = self._arr[1][0] * other._arr[0][0] + self._arr[1][1] * other._arr[1][0]
            x22 = self._arr[1][0] * other._arr[0][1] + self._arr[1][1] * other._arr[1][1]
            x23 = self._arr[1][0] * other._arr[0][2] + self._arr[1][1] * other._arr[1][2]
            x24 = self._arr[1][0] * other._arr[0][3] + self._arr[1][1] * other._arr[1][3]

            return Matrix24([[x11, x12, x13, x14], [x21, x22, x23, x24]])

        raise TypeError(f"cannot multiply Matrix22 on the right by {type(other)}")

    def __rmul__(self, other: float | int) -> Matrix:  # other * self
        is_number = isinstance(other, float) or isinstance(other, int)
        if not is_number:
            raise TypeError("cannot multiply matrix on the left by anything but a number")

        arr = [[other * self._arr[j][i] for i in range(2)] for j in range(2)]
        return Matrix(arr)

    def __abs__(self) -> float:  # determinant
        pass

    def __str__(self) -> str:
        x = self._arr
        return f"Matrix\n\t\t{x[0][0]}\t{x[0][1]}\n\t\t{x[1][0]}\t{x[1][1]}"

    def inverse(self) -> Matrix:  # should probably also enable self ^ (-1) to call inverse
        pass


class Matrix24(Matrix, dimensions=(2, 4)):
    def __init__(self, array: MatrixLike) -> None:
        pass

    def __add__(self, other: Matrix) -> Matrix:
        pass

    def __mul__(self, other: pygame.Vector2 | Matrix | float | int) -> pygame.Vector2 | Matrix:
        pass

    def __rmul__(self, other: float | int) -> Matrix:
        pass

    def __abs__(self) -> float:
        pass

    def __str__(self) -> str:
        pass

    def inverse(self) -> Matrix:
        pass


class Matrix32(Matrix, dimensions=(3, 2)):
    def __init__(self, array: MatrixLike) -> None:
        super().__init__(array)

    def __add__(self, other: Matrix) -> Matrix:
        pass

    def __mul__(self, other: pygame.Vector2 | Matrix | float | int) -> pygame.Vector2 | Matrix:
        pass

    def __rmul__(self, other: float | int) -> Matrix:
        pass

    def __abs__(self) -> float:
        pass

    def __str__(self) -> str:
        pass

    def inverse(self) -> Matrix:
        pass

    def transpose(self) -> Matrix:
        pass


class Matrix33(Matrix, dimensions=(3, 3)):
    def __init__(self, array: MatrixLike) -> None:
        pass

    def __add__(self, other: Matrix) -> Matrix:
        pass

    def __mul__(self, other: pygame.Vector2 | Matrix | float | int) -> pygame.Vector2 | Matrix:
        pass

    def __rmul__(self, other: float | int) -> Matrix:
        pass

    def __abs__(self) -> float:
        pass

    def __str__(self) -> str:
        pass

    def inverse(self) -> Matrix:
        pass

    def transpose(self) -> Matrix:
        pass


class Matrix34(Matrix, dimensions=(3, 4)):
    def __init__(self, array: MatrixLike) -> None:
        pass

    def __add__(self, other: Matrix) -> Matrix:
        pass

    def __mul__(self, other: pygame.Vector2 | Matrix | float | int) -> pygame.Vector2 | Matrix:
        pass

    def __rmul__(self, other: float | int) -> Matrix:
        pass

    def __abs__(self) -> float:
        pass

    def __str__(self) -> str:
        pass

    def inverse(self) -> Matrix:
        pass

    def transpose(self) -> Matrix:
        pass


class Matrix42(Matrix, dimensions=(4, 2)):
    def __init__(self, array: MatrixLike) -> None:
        pass

    def __add__(self, other: Matrix) -> Matrix:
        pass

    def __mul__(self, other: pygame.Vector2 | Matrix | float | int) -> pygame.Vector2 | Matrix:
        pass

    def __rmul__(self, other: float | int) -> Matrix:
        pass

    def __abs__(self) -> float:
        pass

    def __str__(self) -> str:
        pass

    def inverse(self) -> Matrix:
        pass

    def transpose(self) -> Matrix:
        pass


class Matrix43(Matrix, dimensions=(4, 3)):
    def __init__(self, array: MatrixLike) -> None:
        pass

    def __add__(self, other: Matrix) -> Matrix:
        pass

    def __mul__(self, other: pygame.Vector2 | Matrix | float | int) -> pygame.Vector2 | Matrix:
        pass

    def __rmul__(self, other: float | int) -> Matrix:
        pass

    def __abs__(self) -> float:
        pass

    def __str__(self) -> str:
        pass

    def inverse(self) -> Matrix:
        pass

    def transpose(self) -> Matrix:
        pass


class Matrix44(Matrix, dimensions=(4, 4)):
    def __init__(self, array: MatrixLike) -> None:
        pass

    def __add__(self, other: Matrix) -> Matrix:
        pass

    def __mul__(self, other: pygame.Vector2 | Matrix | float | int) -> pygame.Vector2 | Matrix:
        pass

    def __rmul__(self, other: float | int) -> Matrix:
        pass

    def __abs__(self) -> float:
        pass

    def __str__(self) -> str:
        pass

    def inverse(self) -> Matrix:
        pass

    def transpose(self) -> Matrix:
        pass


if __name__ == "__main__":
    M1 = Matrix([[1, 2, 3], [4, 5, 6]])
    M2 = Matrix([[1, 2], [3, 4], [5, 6]])
    print(M1 * M2)




# class DummyMatrix(Matrix, dimensions=(1, 1)):
#     def __init__(self, array: MatrixLike) -> None:
#         pass
#
#     def __add__(self, other: Matrix) -> Matrix:
#         pass
#
#     def __mul__(self, other: pygame.Vector2 | Matrix | float | int) -> pygame.Vector2 | Matrix:
#         pass
#
#     def __rmul__(self, other: float | int) -> Matrix:
#         pass
#
#     def __abs__(self) -> float:
#         pass
#
#     def __str__(self) -> str:
#         pass
#
#     def inverse(self) -> Matrix:
#         pass
#
#     def transpose(self) -> Matrix:
#         pass
