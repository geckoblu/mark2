"""Minimal PDF renderer compatible with markdown-it."""

import tempfile
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Sequence

from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

from mark2.renderer.context.renderer import ConTeXtRenderer


class PDFRenderer(ConTeXtRenderer):
    """A minimal PDF renderer for markdown-it tokens.

    This renderer extends ConTeXtRenderer to generate PDF output by first
    creating a ConTeXt file and then compiling it to PDF using the context command.
    """

    __output__: str = "pdf"

    def render(self, tokens: Sequence[Token], options: OptionsDict, env: EnvType) -> None:
        """Takes token stream and generates PDF output.

        Args:
            tokens: List of block tokens to render
            options: Parser instance parameters
            env: Additional data from parsed input

        Raises:
            SystemExit: If ConTeXt compilation fails or context command is not found
        """

        output_filename = env.get("output_filename", "-")
        pdf_keep_tex = env.get("pdf_keep_tex", False)

        with tempfile.TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "temp.tex"
            env["output_filename"] = str(p)  # generate .tex in temp file

            super().render(tokens, options, env)

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

            pdf = Path(tmpdir) / "temp.pdf"

            if not pdf.exists():
                print("Error: PDF file was not generated", file=sys.stderr)
                sys.exit(1)

            if output_filename == "-":
                with open(pdf, "rb") as f:
                    sys.stdout.buffer.write(f.read())
            else:
                shutil.copy(pdf, output_filename)
                if pdf_keep_tex:
                    if p.exists():
                        shutil.copy(p, Path(output_filename).with_suffix(".tex"))
                    else:
                        print("Warning: .tex file was not found to keep", file=sys.stderr)
        # directory removed at the end of the with block
