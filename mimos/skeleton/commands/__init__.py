from mimos.skeleton.commands.types import Act, Speak


def act(animation: str):
    return Act(animation)


def speak(text: str):
    return Speak(text)


__all__ = ["act", "speak"]
