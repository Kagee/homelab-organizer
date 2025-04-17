# ruff: noqa: T201, S324, INP001, PLW2901
import hashlib
import logging
from typing import Callable, Final  # noqa: UP035

logger = logging.getLogger(__name__)


def md5(input_string: str) -> str:
    return hashlib.md5(input_string.encode()).hexdigest()


def sha1(input_string: str) -> str:
    return hashlib.sha1(input_string.encode()).hexdigest()


DEFAULT_GRID_SIDE: int = 5
DEFAULT_PIXEL_TYPES: int = 2
DEFAULT_PIXELS = ["██", "  ", "▒▒"]
DEFAULT_HASH_FUNC = sha1


def render_utf8(
    arr: list[list],
    *,
    pixels: list[str] = DEFAULT_PIXELS,
) -> None:
    for row in arr:
        for pos in row:
            print(pixels[pos], end="")
        print()


def string_to_identicon_arr(
    s: str,
    *,
    hash_function: Callable = DEFAULT_HASH_FUNC,
    grid_side: int = DEFAULT_GRID_SIDE,
    pixel_types: int = DEFAULT_PIXEL_TYPES,
    pixels: list[str] = DEFAULT_PIXELS,
) -> list[list]:
    min_grid_size: Final[int] = 5
    if grid_side < min_grid_size or (grid_side % 2 == 0):
        msg = f"grid_size must be >={min_grid_size} and odd"
        raise ValueError(msg)

    min_num_pixels: Final[int] = 2
    if len(pixels) < pixel_types or pixel_types < min_num_pixels:
        msg = (
            "Number of pixels must be "
            f"between {min_num_pixels} and {len(pixels)}"
        )
        raise ValueError(msg)

    arr: list[list] = []
    hash_code = hash_function(s)

    while len(hash_code) < (grid_side * grid_side):
        hash_code = hash_code + hash_function(hash_code)

    logger.debug("Hash code is %s", hash_code)
    half_grid_size_int = (grid_side + 1) // 2

    for row in range(grid_side):
        arr.append([])
        for _ in range(grid_side):
            arr[row].append(0)
        for col in range(half_grid_size_int):
            hash_value = int(hash_code[row * grid_side + col], 16)
            # arr[row].append(hash_value % pixel_types)
            arr[row][col] = hash_value % pixel_types
            arr[row][len(arr[row]) - col - 1] = hash_value % pixel_types
    return arr


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        style="{",
        format="{asctime} [{levelname}] {message} ({name}:{module})",
        handlers=[
            # logging.FileHandler(f"{os.path.basename(__file__)}.log"),
            logging.StreamHandler(),
        ],
    )
    ss = [
        "Hello world",
        # "1234567890",
        # "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
        # "eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        #'-(/%/(#6#¤%"#%&/¤&\'(#¤%&#¤%&"#!)))',
        "",  # Empty string
    ]
    ss = ["A38BB65A64D93D3E38FBD6A55571294122F5AD6C", "FABFABFABFAB"]
    for s in ss:

        def foo(i):
            return i

        arr = string_to_identicon_arr(s, hash_function=foo)
        render_utf8(arr)
