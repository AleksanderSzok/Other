import itertools
import os
import re
from collections import deque
from pathlib import Path


class QueryToSelect:
    """
    help migrate query to select style in SQLAlchemy 2.0
    https://docs.sqlalchemy.org/en/20/changelog/migration_20.html#migration-orm-usage
    """

    def __init__(self, session_name="session", path_to_files="/"):
        self.session_name = session_name
        self.path_to_files = path_to_files
        self.converted = False
        self.pattern = rf"(?P<first>.*)(?P<second>{self.session_name}.query)(?P<third>\(.+\))(?P<fourth>\.\w+\(\))$"
        self.second_group_map = {
            ".one()": f"{self.session_name}.execute(select",
            ".first()": f"{self.session_name}.scalars(select",
            ".count()": f"{self.session_name}.scalars(select(func.count()).select_from(select",
            ".all()": f"{self.session_name}.scalars(select",
        }
        self.fourth_group_map = {
            ".one()": ").scalar_one()\n",
            ".first()": ".limit(1)).first()\n",
            ".count()": ")).one()\n",
            ".all()": ").all()\n",
        }

    @staticmethod
    def get_indentation(line):
        return "".join(itertools.takewhile(lambda x: x == " ", line))

    def process_one_line(self, line, compiled_pattern):
        stripped = line.strip()
        pattern_match = compiled_pattern.search(stripped)
        if pattern_match:
            self.converted = True
            return self.get_indentation(line) + self.pattern_match_group(pattern_match)
        else:
            return line

    def pattern_match_group(self, pattern):
        return (
            pattern.group("first")
            + self.second_group_map[pattern.group("second")]
            + pattern.group("third")
            + self.fourth_group_map[pattern.group("fourth")]
        )

    def convert_file(self, file_name):
        p = re.compile(self.pattern)
        converted_lines = deque()
        with open(file_name) as f:
            for line in f.readlines():
                if line.find(".query(") != -1:
                    converted_lines.append(self.process_one_line(line, p))
                else:
                    converted_lines.append(line)

        if self.converted:
            converted_lines.appendleft("from sqlalchemy import select\n")
            self.converted = False
        with open(file_name, "w") as f:
            f.writelines(converted_lines)

    def process_files(self):
        for root, _, files in os.walk(self.path_to_files):
            for file in files:
                if file.endswith(".py"):
                    self.convert_file(Path(root) / file)


if __name__ == "__main__":
    convert = QueryToSelect()
    convert.process_files()
