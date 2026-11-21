"""Show recorded source-failure evidence, or regenerate answers on the same evidence."""

import argparse
import json
from contextlib import nullcontext
from pathlib import Path

from anthropic import AnthropicFoundry

from src.config import AppConfig
from src.model import PolicyAnswer, generate_answer
from src.terminal import format_answer

RECORDING = Path("evaluation/source_failure_recorded.json")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--live", action="store_true",
        help="Make two Azure calls on the captured evidence; does not rerun retrieval.",
    )
    parser.add_argument(
        "--export-dir", type=Path,
        help="Export the exact broken/corrected source documents for Parts 1 and 6.",
    )
    args = parser.parse_args(argv)
    record = json.loads(RECORDING.read_text())
    if args.export_dir:
        for variant in ("broken", "corrected"):
            for source_path, text in record["corrected_sources"].items():
                relative = Path(source_path).relative_to("corpus")
                target = args.export_dir / variant / "corpus" / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                if variant == "broken" and relative.name == "02_passenger_care_2026.md":
                    text = record["broken_care_source"]
                target.write_text(text)
        print(f"Exported exact demonstration sources to {args.export_dir}")
    context = nullcontext(None)
    if args.live:
        config = AppConfig.from_env()
        try:
            config.validate(require_index=False, require_llm=True)
        except ValueError as error:
            parser.error(str(error))
        context = AnthropicFoundry(
            api_key=config.llm_api_key, base_url=config.llm_base_url, timeout=120.0
        )
    print("LIVE GENERATION ON CAPTURED EVIDENCE" if args.live else "RECORDED LIVE API RESULTS")
    print("Controlled stale export; the original status-only defect was handled correctly.")
    print("Question:", record["manifest"]["question"])
    with context as client:
        for name, label in (
            ("broken_live", "BEFORE: stale rule published as current"),
            ("source_only_repaired_replay", "AFTER: source-only repair, same evidence slots"),
        ):
            stage = record["stages"][name]
            answer = (
                generate_answer(
                    record["manifest"]["question"], stage["evidence"], client,
                    model=config.llm_model, as_of=record["manifest"]["as_of_date"],
                ) if args.live else PolicyAnswer.model_validate(stage["answer"])
            )
            print(f"\n{label}\n{format_answer(answer, stage['evidence'])}")


if __name__ == "__main__":
    main()
