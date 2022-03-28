import subprocess


def say_festival(string):
    subprocess.run(["festival", "--tts"], input=string, text=True)


def say_espeak(string):
    subprocess.run(["espeak", "-ven-us+croak", string], stderr=subprocess.DEVNULL)


say = say_espeak
