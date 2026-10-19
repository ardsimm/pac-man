import sys
from typing import List


class Main:

    @staticmethod
    def main(ac: int, av: List[str]) -> None:
        print("Hi mom!")

if __name__ == "__main__":
    Main.main(len(sys.argv), sys.argv)
