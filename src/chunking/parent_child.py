"""Search bounded children and retain their complete level-two Markdown sections."""

from markdown_it import MarkdownIt

from .base import TextChunk
from .markdown import MarkdownChunker


class ParentChildChunker(MarkdownChunker):
    """Create searchable children linked to complete level-two Markdown sections.

    Children obey the model-token limit and never cross a parent boundary.
    Parent bounds let document preparation retain the full section for later
    answer context; the full parent itself is not sent to the embedding model.
    """

    strategy = "parent-child"

    def chunk_with_offsets(self, text: str) -> list[TextChunk]:
        """Return bounded children with child and parent offsets in the original text.

        Each h2 heading starts a parent that ends at the next h2 or document end.
        Any introductory text forms its own parent. Split each parent using the
        Markdown strategy, then translate its children's offsets back to the
        document. Without h2 headings, fall back to ordinary Markdown chunks
        with no parent metadata. Blank input returns [].
        """
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
            # Split each parent independently so a child cannot mix neighboring chapters.
            for child in super().chunk_with_offsets(text[start:end]):
                # Child offsets were local to the parent slice; stored offsets are global.
                chunks.append(
                    TextChunk(child.text, start + child.start, start + child.end, start, end)
                )
        return chunks
