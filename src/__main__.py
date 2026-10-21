import sys
from typing import List
from src.render.garbage import test


class Main:
    @staticmethod
    def main(ac: int, av: List[str]) -> None:
        test()


if __name__ == "__main__":
    Main.main(len(sys.argv), sys.argv)
