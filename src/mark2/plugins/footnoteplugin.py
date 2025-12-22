"""The content of this file is adapted from mdit-py-plugins footnote plugin,
with modifications to change the placement of footnote tokens in the token stream."""

# pylint: disable=invalid-name  # Because of the naming conventions in markdown-it-py

from typing import Sequence

from markdown_it.renderer import RendererProtocol
from markdown_it.rules_core import StateCore
from markdown_it.utils import EnvType, OptionsDict
from markdown_it.token import Token

from mdit_py_plugins.footnote.index import _data_from_env


def footnote_tail(state: StateCore) -> None:
    """Post-processing step, to move footnote tokens to end of the token stream.

    Also removes un-referenced tokens.
    """

    insideRef = False
    refTokens = {}

    if "footnotes" not in state.env:
        return

    current: list[Token] = []
    tok_filter = []
    for tok in state.tokens:
        if tok.type == "footnote_reference_open":
            insideRef = True
            current = []
            currentLabel = tok.meta["label"]
            tok_filter.append(False)
            continue

        if tok.type == "footnote_reference_close":
            insideRef = False
            # prepend ':' to avoid conflict with Object.prototype members
            refTokens[":" + currentLabel] = current
            tok_filter.append(False)
            continue

        if insideRef:
            current.append(tok)

        tok_filter.append(not insideRef)

    state.tokens = [t for t, f in zip(state.tokens, tok_filter, strict=False) if f]

    footnote_data = _data_from_env(state.env)
    if not footnote_data["list"]:
        return

    token = Token("footnote_block_open", "", 1)
    state.tokens.append(token)

    for i, foot_note in footnote_data["list"].items():  # pylint: disable=too-many-nested-blocks
        token = Token("footnote_open", "", 1)
        token.meta = {"id": i, "label": foot_note.get("label", None)}
        # TODO propagate line positions of original foot note # pylint: disable=fixme
        # (but don't store in token.map, because this is used for scroll syncing)
        state.tokens.append(token)

        if "tokens" in foot_note:
            tokens = []

            token = Token("paragraph_open", "p", 1)
            token.block = True
            tokens.append(token)

            # Add footnote_anchor tokens here, before inline content
            t = foot_note["count"] if (("count" in foot_note) and (foot_note["count"] > 0)) else 1
            j = 0
            while j < t:
                token = Token("footnote_anchor", "", 0)
                token.meta = {"id": i, "subId": j, "label": foot_note.get("label", None)}
                tokens.append(token)
                j += 1

            token = Token("inline", "", 0)
            token.children = foot_note["tokens"]
            token.content = foot_note["content"]
            tokens.append(token)

            token = Token("paragraph_close", "p", -1)
            token.block = True
            tokens.append(token)

        elif "label" in foot_note:
            tokens = refTokens.get(":" + foot_note["label"], [])
            # For reference footnotes, insert anchors after paragraph_open
            if tokens:
                # Find the paragraph_open token
                for idx, tok in enumerate(tokens):
                    if tok.type == "paragraph_open":
                        # Insert footnote_anchor tokens after paragraph_open
                        t = (
                            foot_note["count"]
                            if (("count" in foot_note) and (foot_note["count"] > 0))
                            else 1
                        )
                        anchor_tokens = []
                        j = 0
                        while j < t:
                            token = Token("footnote_anchor", "", 0)
                            token.meta = {
                                "id": i,
                                "subId": j,
                                "label": foot_note.get("label", None),
                            }
                            anchor_tokens.append(token)
                            j += 1
                        tokens = tokens[: idx + 1] + anchor_tokens + tokens[idx + 1 :]
                        break

        state.tokens.extend(tokens)

        token = Token("footnote_close", "", -1)
        state.tokens.append(token)

    token = Token("footnote_block_close", "", -1)
    state.tokens.append(token)

    # Helper methods (return values, used by other render rules)


def render_footnote_anchor_name(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    """Generate footnote anchor ID.
    The anchor name is used in HTML id and href attributes for linking."""
    n = str(tokens[idx].meta["id"] + 1)
    prefix = ""

    doc_id = env.get("docId", None)
    if isinstance(doc_id, str):
        prefix = f"-{doc_id}-"

    return prefix + n


def render_footnote_caption(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    """Generate footnote caption text.
    The caption is what's displayed to users (the visible number)."""
    n = str(tokens[idx].meta["id"] + 1)

    if tokens[idx].meta.get("subId", -1) > 0:
        n += ":" + str(tokens[idx].meta["subId"])

    return n
