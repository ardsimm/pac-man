from typing import List

from pydantic import ValidationError
from pydantic_core import from_json

from src.config import Config
from src.parser.parser_exceptions import ParsingError


class Parser:

    def __strip_comments(self, lines: List[str]) -> List[str]:
        stripped_lines: List[str] = []

        for line in lines:
            if line.strip().startswith("#"):
                continue
            if "#" in line:
                stripped_lines.append(line[: line.index("#")])
            else:
                stripped_lines.append(line)
        return stripped_lines

    def parse_config(self, file_path: str) -> Config:
        try:
            with open(file_path) as file:
                file_content = file.read()
                file_lines = file_content.split("\n")
                stripped_file_lines = self.__strip_comments(file_lines)
                json_data = from_json("\n".join(stripped_file_lines))
                return Config.model_validate(json_data)
        except OSError as error:
            raise ParsingError(error)
        except ValidationError as error:
            raise ParsingError(error)
