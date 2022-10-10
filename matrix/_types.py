from typing import List, Tuple, Dict, Any, TypeAlias, TypeVar

Numeric = float | int
MatrixLike: TypeAlias = List[List[Numeric]]
DimLike: TypeAlias = Tuple[int, int]

TwoTall: TypeAlias = TypeVar("Matrix22") | TypeVar("Matrix23") | TypeVar("Matrix24")
ThreeTall: TypeAlias = TypeVar("Matrix32") | TypeVar("Matrix33") | TypeVar("Matrix34")
FourTall: TypeAlias = TypeVar("Matrix42") | TypeVar("Matrix43") | TypeVar("Matrix44")