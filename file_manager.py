import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional


@dataclass
class FileObj:
    name: str
    path: str
    size: int
    created: datetime
    modified: datetime
    is_directory: bool

    def __lt__(self, other) -> bool:
        return self.created < other.created

    def __str__(self) -> str:
        return f""""
            Name: {self.name}
            Path: {self.path}
            Size: {self.size}
            Created: {self.created}
            Modified: {self.modified}
            Is_directory: {self.is_directory}
        """


class FileManager:
    def __init__(self):
        self.entries: List[FileObj] = []

    def get_files_names(self, path: str = os.getcwd()) -> None:
        for root, dirs, files in os.walk(path):
            for name in files + dirs:
                new_path = Path(root) / name
                entry = FileObj(
                    name=name,
                    path=root,
                    size=os.path.getsize(new_path),
                    created=datetime.fromtimestamp(os.path.getctime(new_path)),
                    modified=datetime.fromtimestamp(os.path.getmtime(new_path)),
                    is_directory=name in dirs,
                )
                self.entries.append(entry)

    @staticmethod
    def create_dirs(
        number_of_folders: int, levels: int = 2, path: Path = Path(os.getcwd())
    ) -> None:
        if levels == 0:
            return
        for i in range(number_of_folders):
            dir_path = Path(path) / chr(i + 65)
            try:
                os.makedirs(dir_path)
            except FileExistsError:
                pass
            FileManager.create_dirs(number_of_folders, levels - 1, path=dir_path)

    def __str__(self) -> str:
        return "".join([str(entry) for entry in self.entries])

    def sort_file_stats(self, count: Optional[int] = None) -> List[FileObj]:
        if not count:
            count = len(self.entries)
        return sorted(self.entries, reverse=True)[:count]


file_stats = FileManager()
# file_stats.get_files_names()
# print(file_stats)
# try:
#     number_of_entries = int(sys.argv[1])
# except IndexError:
#     number_of_entries = None
# print(file_stats.sort_file_stats(number_of_entries))
file_stats.create_dirs(1)