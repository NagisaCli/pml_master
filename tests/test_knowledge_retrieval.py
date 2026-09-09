"""
Retrieval ranking tests.

``test_skill_integrity.test_knowledge_base_loads_the_skill_corpus`` checks that
three canonical queries land on the right document. That is a symptom test: it
says the ranking is wrong today, not which rule is wrong, and it passes or fails
according to how the real corpus happens to be shaped.

It was not enough. ``search()`` scored raw term frequency, so relevance was
partly a proxy for document length; the JK_Pump_Build log grew past the Iron
Rules and began winning datum queries. The fix was written up in that log as
done and never implemented, and the symptom test stayed red for thirteen
commits while the log kept growing.

These tests pin the two ranking rules directly, against a synthetic corpus, so
they fail for a stated reason and do not depend on the real corpus's shape.
"""

from __future__ import annotations

import pytest

from pml_knowledge.knowledge_base import PMLKnowledgeBase


@pytest.fixture
def corpus(tmp_path):
    """Build a knowledge base from a corpus whose shape the test controls."""

    def _build(docs: dict) -> PMLKnowledgeBase:
        for name, text in docs.items():
            path = tmp_path / f"{name}.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        return PMLKnowledgeBase(corpus_dir=tmp_path)

    return _build


#: Filler documents exist only to give ``statistics.median`` something
#: meaningful to measure against. A two-document corpus has a median halfway
#: between its two members, which is not a yardstick.
FILLER = {
    f"workflows/filler-{n}": f"# Filler {n}\n\n" + ("unrelated prose line\n" * 30)
    for n in range(5)
}


# --- Length must not buy relevance ---------------------------------------

def test_a_long_log_does_not_outrank_a_short_authority_on_length_alone(corpus):
    """
    The exact failure that went unnoticed for thirteen commits.

    The log is three times longer than the authority and mentions the query
    terms half again as often -- but at *lower density*, purely as a
    consequence of its size. Its extra mentions are incidental; the authority
    is the document actually about the rule. Raw term frequency ranks the log
    first because it counts mentions, not aboutness.

    Note what this test does not claim. ``sqrt`` damping is a correction, not a
    cure: a document that genuinely repeats a term far more often than the
    authority still wins, and ``_length_factor`` says so in as many words. What
    must not happen is a document winning on size at equal or lower density.
    """
    unit = "the datum sits at the centre of the primitive\n"
    filler = "an unrelated sentence about bracket fabrication\n"

    authority = "# Rules\n\n" + (unit * 12) + (filler * 28)
    log = "# Round-by-round record\n\n" + (unit * 18) + (filler * 102)

    docs = {"knowledge/datum-rules": authority, "projects/long-log": log}
    docs.update(FILLER)
    kb = corpus(docs)

    authority_len = len(kb.documents["knowledge/datum-rules"])
    log_len = len(kb.documents["projects/long-log"])
    assert log_len > 2.5 * authority_len, "log is not long enough to bias"
    assert log.count("datum") > authority.count("datum"), (
        "raw term frequency must favour the log, or the test proves nothing"
    )
    assert (
        log.count("datum") / log_len < authority.count("datum") / authority_len
    ), "the log must be the less dense document, or it deserves to win"

    top = kb.search("centre datum", top_k=1)
    assert top[0]["source"] == "knowledge/datum-rules", (
        "a longer, less dense document won on term count alone; "
        "_length_factor is not damping term frequency"
    )


def test_a_short_document_is_not_boosted_for_being_short(corpus):
    """
    Normalisation must only penalise longer-than-median documents, never
    reward shorter ones. Uncapped, the length factor exceeds 1.0 for every
    file below the median -- a bias in the other direction, cancelling the
    first by accident rather than by design, and one that would hand unrelated
    stub documents the top spot on thin queries.

    Both documents below sit under the median, mention the term exactly once,
    and carry the same heading, so neither may be damped and neither may be
    lifted: their scores must be equal. Uncapped normalisation lifts the
    shorter one well clear on length alone.
    """
    padding = "an unrelated sentence carrying no query term at all\n"
    docs = {
        "a/short": "# Subject\n\nnozzle\n",
        "b/larger": "# Subject\n\nnozzle\n" + (padding * 40),
    }
    # Filler longer than both, so the median sits above them and neither is
    # penalised. Any difference in their scores is then a boost, not damping.
    docs.update(
        {
            f"workflows/filler-{n}": f"# Filler {n}\n\n" + (padding * 60)
            for n in range(5)
        }
    )
    kb = corpus(docs)

    assert len(kb.documents["a/short"]) < len(kb.documents["b/larger"])
    for doc in ("a/short", "b/larger"):
        assert kb.documents[doc].count("nozzle") == 1

    ranked = {r["source"]: r["relevance"] for r in kb.search("nozzle", top_k=20)}
    assert ranked["a/short"] == pytest.approx(ranked["b/larger"]), (
        "identical evidence scored differently on length alone; normalisation "
        "is boosting the short file instead of only damping long ones"
    )


# --- Routing must be an intent decision, not a bonus ---------------------

def test_routing_outranks_a_document_of_any_size(corpus):
    """
    A flat bonus is always one entry away from being overtaken: term frequency
    grows without bound as a log accumulates rounds, a constant does not. The
    +750 that used to sit in ``search`` was overrun exactly this way.

    The competitor here is stuffed with the query's own words so that no fixed
    bonus could survive it. Routing must still win, because routing expresses
    what the user asked for.
    """
    stuffed = "# Bulk\n\n" + (
        "shape spatial intent choose element construct selection\n" * 4000
    )
    kb = corpus(
        {
            "knowledge/pml-spatial-lookup": "# Spatial lookup\n\nChoose by shape.\n",
            "projects/bulk": stuffed,
        }
    )

    top = kb.search("choose element for shape and spatial intent", top_k=1)
    assert top[0]["source"] == "knowledge/pml-spatial-lookup", (
        "routing lost to a large document; _route_to is adding a bonus rather "
        "than lifting above the leader"
    )


def test_routing_survives_a_document_that_grows(corpus):
    """
    Regression on the mechanism rather than a threshold. A bonus-based
    implementation passes at 100 lines and fails at 10,000; lifting above the
    leader holds at every size, which is the property that matters as project
    logs accumulate rounds.
    """
    target = "workflows/learning-from-native-exports"
    for lines in (100, 1_000, 10_000):
        kb = corpus(
            {
                target: "# Learning from native exports\n\nPromotion gates.\n",
                "projects/growing": "# Growing\n\n"
                + ("native export syntax study of a shape\n" * lines),
            }
        )
        assert target in kb.documents, "routing target missing from corpus"
        top = kb.search("native export syntax experiment", top_k=1)
        assert top[0]["source"] == target, (
            f"routing lost to a {lines}-line competitor; _route_to is not "
            f"lifting above the leader"
        )


def test_routing_is_a_no_op_when_the_target_is_absent(corpus):
    """Routing to a document the corpus does not contain must not invent it."""
    kb = corpus({"projects/only": "# Only\n\nchoose a shape by spatial intent\n"})
    top = kb.search("choose element for shape and spatial intent", top_k=1)
    assert top[0]["source"] == "projects/only"
    assert "knowledge/pml-spatial-lookup" not in kb.documents
