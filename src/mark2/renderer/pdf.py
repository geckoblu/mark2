"""Minimal PDF renderer compatible with markdown-it."""

import argparse
import sys
import tempfile
import subprocess
import shutil
from pathlib import Path

from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

from mark2.renderer.base import Renderer
from mark2.renderer.context import ConTeXtRenderer


class PDFRenderer(Renderer):
    """A minimal PDF renderer for markdown-it tokens."""

    def __init__(self, args: argparse.Namespace, options: OptionsDict, env: EnvType) -> None:
        """Initialize the PDF renderer.

        This renderer uses ConTeXt to generate PDFs from markdown-it tokens.
        """
        super().__init__(args, options, env)

        self.args = args

    def render(
        self,
        tokens: list[Token],
        output_filename: str,
    ) -> None:
        """Render markdown-it tokens to PDF via ConTeXt.

        This method first converts the tokens to ConTeXt format in a temporary file,
        then compiles it to PDF using the 'context' command.

        Args:
            tokens: List of tokens from markdown-it parser
            output_filename: Output file path (use '-' for stdout to write binary PDF)

        Raises:
            SystemExit: If ConTeXt is not installed or compilation fails
        """

        with tempfile.TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "temp.tex"
            ConTeXtRenderer(self.args, self.options, self.env).render(tokens, str(p))

            try:
                result = subprocess.run(
                    ["context", str(p)], cwd=tmpdir, capture_output=True, text=True, check=False
                )

                if result.returncode != 0:
                    print(
                        f"Error: ConTeXt compilation failed with code {result.returncode}",
                        file=sys.stderr,
                    )
                    if result.stderr:
                        print(result.stderr, file=sys.stderr)
                    sys.exit(1)
            except FileNotFoundError:
                print(
                    "Error: 'context' command not found. Please install ConTeXt to generate PDFs.",
                    file=sys.stderr,
                )
                print(
                    "Visit https://wiki.contextgarden.net/Introduction/Installation#Installation for installation instructions.",  # pylint: disable=line-too-long
                    file=sys.stderr,
                )
                sys.exit(1)

            # print("Files in tmpdir after subprocess:")
            # for file in Path(tmpdir).iterdir():
            #     print(f"  {file.name}")

            pdf = Path(tmpdir) / "temp.pdf"

            if not pdf.exists():
                print("Error: PDF file was not generated", file=sys.stderr)
                sys.exit(1)

            if output_filename == "-":
                with open(pdf, "rb") as f:
                    sys.stdout.buffer.write(f.read())
            else:
                shutil.copy(pdf, output_filename)
        # directory removed at the end of the with block
