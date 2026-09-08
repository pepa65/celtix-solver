import os
import sys
import cv2 as cv

from model import solve_puzzle
from graphics import parse_image, draw_solution
from textics import parse_csv_puzzle, print_solution


if len(sys.argv) > 1:
    sys.argv[1] = f"/w/{sys.argv[1]}"
if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
    print(f"Usage: {sys.argv[0]} puzzle.file", file=sys.stderr)
    print(f"  The puzzle file can be either a PNG screenshot or CSV", file=sys.stderr)
    sys.exit(1)

if open(sys.argv[1], "rb").read(6).decode("latin1").lower() == "celtix":

    puzzle = parse_csv_puzzle(open(sys.argv[1]))
    print(puzzle)
    solution = solve_puzzle(puzzle)
    print_solution(solution)

else:

    image = cv.imread(sys.argv[1], cv.IMREAD_COLOR)
    if image is None:
        print(f"Cannot read image at {sys.argv[1]!r}", file=sys.stderr)
        sys.exit(1)
    puzzle, grid = parse_image(image)
    print(puzzle)
    solution = solve_puzzle(puzzle)
    print_solution(solution)
    drawn = draw_solution(image, grid, solution)
    out = f"/w/{sys.argv[2]}" if len(sys.argv) > 2 else "/w/output.png"
    cv.imwrite(out, drawn)
    stat = os.stat(sys.argv[1])
    os.chown(out, stat.st_uid, stat.st_gid)
