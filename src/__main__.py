import sys
from traceback import print_exception
from typing import List

from src.engine.engine import Engine
from src.parser.parser import Parser
from src.parser.parser_exceptions import ParsingError


class Main:
    @staticmethod
    def main(ac: int, av: List[str]) -> int:
        if ac != 2:
            print("Invalid usage, usage:\nuv run python -m src [config_file]")
            return 1
        try:
            config = Parser().parse_config(av[1])
            print(config)
        except ParsingError as err:
            print(sys.stdout, f"Parsing error:\n{err}")
            return 1
        Engine().run()
        return 0


if __name__ == "__main__":
    try:
        sys.exit(Main.main(len(sys.argv), sys.argv))
    except KeyboardInterrupt:
        print("Interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print("An unhandled error occured:", file=sys.stderr)
        print_exception(e)
        sys.exit(1)
