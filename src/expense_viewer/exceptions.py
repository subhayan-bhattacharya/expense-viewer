class Error(Exception):
    def __init__(self, message) -> None:
        self.message = message

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"


class FileOrDirectoryNotFound(Error):
    """Missing file or directory."""


class CouldNotLoadYamlFileError(Error):
    """When a yaml file could not be loaded."""


class WrongFormatError(Error):
    """Wrong format of file supplied."""


class CouldNotLoadSalaryStmtError(Error):
    """When a salary statement could not be loaded."""
