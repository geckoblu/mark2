"""Extended argparse file type with file extension checking."""

from argparse import ArgumentTypeError
import os
from typing import Optional, Union


class FileType:
    """Extended argparse FileType that checks file extensions."""

    def __init__(self, mode: str = "r", extension: Optional[Union[str, list[str]]] = None) -> None:
        """Initialize FileType with mode and optional extension filter.

        Args:
            mode: File open mode ('r' for read, 'w' for write)
            extension: Optional extension(s) to validate (string or list of strings)
        """
        self._mode = mode
        if extension is None:
            self._extension = None
        elif isinstance(extension, list):
            self._extension = [ext.lower() for ext in extension]
        else:
            self._extension = [ext.lower() for ext in extension.split(",")]

    def __call__(self, string: str) -> str:
        """Open a file with the given mode and check its extension."""

        # the special argument "-" means sys.std{in,out}
        if string == "-":
            return "-"

        # all other arguments are used as file names
        filename = os.path.expanduser(string)

        if "r" in self._mode:
            if not os.path.exists(filename):
                raise ArgumentTypeError(f"doesn't exist: '{string}'")
            if not os.path.isfile(filename):
                raise ArgumentTypeError(f"not a file: '{string}'")
            if self._extension:
                __, ext = os.path.splitext(filename)
                if ext.startswith("."):
                    ext = ext[1:]
                if ext.lower() not in self._extension:
                    if len(self._extension) == 1:
                        raise ArgumentTypeError(f"not a '{self._extension[0]}' file: '{string}'")
                    else:
                        raise ArgumentTypeError(f"not an '{self._extension}' file: '{string}'")

        # Try to open but close immediately
        try:
            with open(filename, self._mode, encoding="utf-8") as _fp:
                return filename
        except OSError as ex:
            raise ArgumentTypeError(f"can't open: {ex}") from ex
