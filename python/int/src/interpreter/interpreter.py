from pathlib import Path
from typing import TextIO


class Interpreter:
    """
    The main interpreter class, responsible for loading the source file and executing the program.
    """

    def load_program(self, source_file: Path) -> None:
        """
        Reads the source SOL-XML file and stores it as the target program for this interpreter.
        If any program was previously loaded, it is replaced by the new one.
        """


    def execute(self, input_io: TextIO) -> None:
        """
        Executes the currently loaded program, using the provided input stream as standard input.
        """
