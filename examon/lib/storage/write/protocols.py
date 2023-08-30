from typing_extensions import Protocol


class FileWriter(Protocol):
    def create_files(self) -> None: ...

    def delete_files(self) -> None: ...


class ContentWriter(Protocol):
    def create_all(self) -> None: ...
