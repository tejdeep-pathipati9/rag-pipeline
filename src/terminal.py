"""Terminal prompt and answer display."""

from anthropic import APIError
from pinecone.errors import PineconeError

from src.model import PolicyAnswer, generate_answer
from src.retrieval import TOP_K, assemble_evidence, rerank_results, retrieve_hybrid


def format_answer(answer: PolicyAnswer, matches: list[dict]) -> str:
    """Show the answer, source titles and sections, and any missing information."""
    titles = {hit["document_id"]: hit["title"] for hit in matches if "title" in hit}
    lines = [answer.answer]
    if answer.citations:
        lines.append("Sources")
        for citation in dict.fromkeys(answer.citations):
            doc, _, section = citation.partition("#")
            label = f"{titles[doc]} ({doc})" if doc in titles else doc
            lines.append(f"  - {label}, §{section}")
    if answer.missing_information:
        lines.append("Still needed")
        lines.extend(f"  - {item}" for item in answer.missing_information)
    return "\n".join(lines)


def interactive_session(
    embeddings, index, reranker, client, *, namespace: str, model: str, top_k: int = TOP_K
):
    """Keep the models and clients open while answering questions from the terminal."""
    print("\nNorthstar Policy Q&A\nAsk a question, type /help for examples, or exit to leave.\n")
    while True:
        try:
            question = input("You> ").strip()
            command = question.casefold()
            if command in {"exit", "quit", "/exit", "/quit"}:
                break
            if not question:
                continue
            if command in {"help", "/help"}:
                print(
                    "\nTry: Will Northstar pay for a hotel after a weather delay?\n"
                    "     Can I get a refund if I turn down the replacement flight?\n"
                    "Type exit or press Ctrl-D to leave.\n"
                )
                continue
            print("Looking up the policy...", flush=True)
            candidates = retrieve_hybrid(
                question, embeddings, index, namespace=namespace, top_k=top_k
            )
            ranked = rerank_results(question, candidates, reranker)
            evidence = assemble_evidence(ranked, embeddings.tokenizer)
            answer = generate_answer(question, evidence, client, model=model)
            print(f"\nNorthstar:\n{format_answer(answer, evidence)}\n")
        except (EOFError, KeyboardInterrupt):
            break
        except (APIError, PineconeError, ValueError, RuntimeError):
            print("\nUnable to complete that answer. Please try again or rephrase your question.\n")
    print("\nGoodbye.")
