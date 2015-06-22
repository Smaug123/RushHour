# RushHour
This repository should ultimately contain a solver for Rush Hour. Currently it contains a data structure only.

## Board data structure
The board assumes wlog that the exit is on the right-hand edge. Therefore, the exit point exit_position is given only as an integer, determining how far from the top the exit is. For instance, an exit on the top-right corner's right edge would be given by index 0.

The blocks_num attribute holds the number of blocks; the board attribute is a 2d array of integers (0 for an empty space, then an integer for each different piece).

The board_width and board_height attributes are integers representing the width and height.

The board comes with a slide_piece method, which alters the board in-place to move the specified piece in the specified direction.

### Example
000020
000020
001120|
000300
000344
000000

The pipe symbol shows where the exit is. (The solution to this puzzle is to move piece 1 left, then 3 up two, then 4 left two, then 2 down three, then 1 right four.)

This structure would have board_width == board_height == 2, and exit_position == 2, blocks_num == 4.

[Rush Hour Wikipedia]: https://en.wikipedia.org/wiki/Rush_Hour_(board_game)