# celtix-solver
**Automatically solve Celtix puzzles**

* License: Public Domain
* Repo: https://github.com/pepa65/celtix-solver
* After: https://github.com/amirlb/celtix-solver

Why would you want to do that? Are you trying to cheat your friends? Or do you want to spoil the puzzle for yourself?

[Celtix](https://www.andrewt.net/puzzles/celtix/?p=3) is a fun new puzzle by [Andrew Taylor](https://www.andrewt.net/).

[Amir] I've been wanting to learn to use OpenCV and Python MIP for a while, so here we go.

## Usage instructions
Take a screenshot (white background, so no Dark mode!), or use the one in the examples directory.

### Clone the repo
```
git clone https://github.com/pepa65/celtix-solver
cd celtix-solver
```

And then either run the solver in a virtual environent, or use docker.

#### Run the solver in a virtual environment
* Prepare the environment:
  - `python3 -m venv .`  (package `python3-venv` should be instaled)
  - `bin/pip install -r requirements.txt`
* Run example: `bin/python3 main.py examples/puzzle3.png`

### Use docker
* Build the image: `docker build -t celtix .`
* Run: `docker run --rm -v .:/w -w /w celtix PUZZLE SOLUTION`
  - Replace `PUZZLE` with a image file in the current tree (like `examples/puzzle3.png`)
  - Replace `SOLUTION` with a different name, or leave it off (it will default to `output.png`)
* Use this `celtix` alias for convenience:  celtix PUZZLE SOLUTON.png
  `alias celtix='docker run --rm -v .:/w -w /w celtix'`

Wait for 1-10 minutes (or many hours) or so it finds a solution, and the image will appear.
