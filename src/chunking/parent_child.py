"""Search bounded children and retain their complete level-two Markdown sections."""

from markdown_it import MarkdownIt

from .base import TextChunk
from .markdown import MarkdownChunker


class ParentChildChunker(MarkdownChunker):
    """Keep children inside a single parent; parent text is not embedded or truncated."""

    strategy = "parent-child"

    def chunk_with_offsets(self, text: str) -> list[TextChunk]:
        line_starts = [0]
        for line in text.splitlines(keepends=True):
            line_starts.append(line_starts[-1] + len(line))
        boundaries = {0, len(text)}
        has_sections = False
        for token in MarkdownIt("commonmark").parse(text):
            if token.type == "heading_open" and token.tag == "h2" and token.map is not None:
                has_sections = True
                boundaries.add(line_starts[token.map[0]])
        if not has_sections:
            return super().chunk_with_offsets(text)

        positions = sorted(boundaries)
        chunks = []
        for start, end in zip(positions[:-1], positions[1:], strict=True):
            for child in super().chunk_with_offsets(text[start:end]):
                chunks.append(
                    TextChunk(child.text, start + child.start, start + child.end, start, end)
                )
        return chunks
