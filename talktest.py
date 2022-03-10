import subprocess
import time
from whackamole import say_espeak, say_festival


def compare(string):
    for fn in [say_espeak, say_festival]:
        start = time.perf_counter()
        fn(string)
        print(f"Took {time.perf_counter()-start:.2f}s")


compare("Hello")

compare("Hit the first mole to start")

compare("3.45 seconds. You got the new high score")
