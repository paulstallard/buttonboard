import buttonboard
import curses
from say import say
import simon
import whackamole


class Game:
    def __init__(self, title):
        self.title = title
        self.hs_filename = f".highscore_{title.lower()}"
        self.high_score = self.init_high_score()
        self.last_score = None

    def init_high_score(self):
        try:
            with open(self.hs_filename) as f:
                return float(f.read())
        except (FileNotFoundError, ValueError):
            return None

    def set_high_score(self, hs):
        self.high_score = hs
        with open(self.hs_filename, "w") as f:
            f.write(f"{hs}\n")

    @property
    def last_str(self):
        return f"Last: {self.display_last}"

    @property
    def best_str(self):
        return f"Best: {self.display_best}"


class SimonGame(Game):
    def __init__(self):
        super().__init__("Simon")

    def play(self, board):
        score = simon.simon_game(board)
        self.last_score = score
        say(f"Your score was {score}")
        if not self.high_score or score > self.high_score:
            say("Congratulations, that's a new high score")
            self.set_high_score(score)
        else:
            say(f"The high score remains at {self.high_score}")

    @property
    def display_last(self):
        return f"{self.last_score:.0f}" if self.last_score else "---"

    @property
    def display_best(self):
        return f"{self.high_score:.0f}" if self.high_score else "---"


class WhackamoleGame(Game):
    def __init__(self):
        super().__init__("Whack-a-mole")

    def play(self, board):
        elapsed_time = whackamole.whackamole(board)
        self.last_score = elapsed_time

        say(f"{elapsed_time:.2f} seconds,,,")

        if not self.high_score:
            say("you have set the first highscore")
            self.set_high_score(elapsed_time)
        else:
            diff_to_hs = round(elapsed_time - self.high_score, 2)
            if diff_to_hs > 0:
                say(f"Bad luck, you missed the high score by {diff_to_hs:.2f} seconds")
            elif diff_to_hs < 0:
                say(f"Well done, you beat the high score by {-diff_to_hs:.2f} seconds")
                self.set_high_score(elapsed_time)
            else:
                say("you have equaled the high score")

    @property
    def display_last(self):
        return f"{self.last_score:.2f} seconds" if self.last_score else "---"

    @property
    def display_best(self):
        return f"{self.high_score:.2f} seconds" if self.high_score else "---"


def show_stuff(win, title, last_str, best_str, col):
    y, x = win.getmaxyx()
    win.clear()
    win.attron(col)
    win.border()
    win.attroff(col)
    win.addstr(0, 0, f" {title.upper()} ", col | curses.A_REVERSE)
    win.addstr(4, 10, last_str, col)
    win.addstr(6, 10, best_str, col)


def show_screen(stdscr, games):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    curses.curs_set(False)
    y, x = stdscr.getmaxyx()

    for n, g in enumerate(games):
        win = stdscr.subwin(10, x, 12 * n, 0)
        show_stuff(win, g.title, g.last_str, g.best_str, curses.color_pair(n + 1))

    stdscr.refresh()


def game_select(board):
    board.light_on(0)
    board.light_on(4)
    while True:
        choice = board.get_buttons()
        if 0 in choice:
            board.board_clear()
            return 0
        elif 4 in choice:
            board.board_clear()
            return 1


def main(stdscr):
    games = [WhackamoleGame(), SimonGame()]

    board = buttonboard.ButtonBoard()

    while True:
        show_screen(stdscr, games)
        choice = game_select(board)
        games[choice].play(board)


curses.wrapper(main)
