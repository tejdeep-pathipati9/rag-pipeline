"""Keep Markdown sections and complete blocks together where the token budget allows."""

from markdown_it import MarkdownIt

from .base import TextChunk
from .recursive import RecursiveChunker


class MarkdownChunker(RecursiveChunker):
    """Pack complete sections, splitting long sections into their Markdown blocks.

    A paragraph or table that fits stays in one chunk, including its original text.
    Overlap applies to recursive fallback inside a long block, where splitting is
    necessary. Each chunk still points to one contiguous slice of the source.
    """

    strategy = "markdown"

    def chunk_with_offsets(self, text: str) -> list[TextChunk]:
        """Build source slices along parsed heading, paragraph, table and other block boundaries."""
        line_starts = [0]
        for line in text.splitlines(keepends=True):
            line_starts.append(line_starts[-1] + len(line))

        # Parsing the whole document keeps fenced text out of the heading list.
        headings = {0, len(text)}
        blocks = set()
        for token in MarkdownIt("commonmark").enable("table").parse(text):
            if token.level == 0 and token.map is not None:
                start = line_starts[token.map[0]]
                blocks.add(start)
                if token.type == "heading_open":
                    headings.add(start)

        # Keep a section whole if it fits. Within a long section, pack entire blocks instead.
        sections = sorted(headings)
        boundaries = [0]
        for start, end in zip(sections[:-1], sections[1:], strict=True):
            if len(self.tokenizer.encode(text[start:end])) > self.chunk_size:
                boundaries.extend(sorted(block for block in blocks if start < block < end))
            boundaries.append(end)

        # Combine adjacent units to avoid fills consisting of only small headings or clauses.
        chunks = []
        pending = 0
        for start, end in zip(boundaries[:-1], boundaries[1:], strict=True):
            if start > pending and len(self.tokenizer.encode(text[pending:end])) > self.chunk_size:
                chunks.extend(self._split_at_offset(text[pending:start], pending))
                pending = start

        chunks.extend(self._split_at_offset(text[pending:], pending))
        return chunks

    def _split_at_offset(self, text: str, offset: int) -> list[TextChunk]:
        """Translate the shared splitter's positions back to the original document."""
        return [
            TextChunk(chunk.text, chunk.start + offset, chunk.end + offset)
            for chunk in super().chunk_with_offsets(text)
        ]
