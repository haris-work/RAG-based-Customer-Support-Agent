
import csv
import json
import uuid

from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from agents.customerSupportAgent import RunCustomerSupportAgent


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = (
    BASE_DIR / "evaluations" / "supportEvaluationCases.json"
)

RESULTS_DIR = BASE_DIR / "evaluations" / "results"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def MockCreateTicket(thread_id, customer_message, intent):

    return {
        "created": True,
        "ticket": {
            "ticket_id": "NT-EVALUATION",
            "thread_id": thread_id,
            "customer_message": customer_message,
            "intent": intent,
            "status": "pending"
        }
    }


def MockNotification(ticket_id):

    return {
        "ticket_id": ticket_id,
        "delivery_status": "sent",
        "http_status": 200
    }


def RunEvaluation():

    cases = json.loads(
        DATASET_PATH.read_text(encoding="utf-8")
    )

    results = []

    print(f"\nRunning {len(cases)} evaluation cases\n")

    for index, case in enumerate(cases, start=1):

        print(
            f"[{index}/{len(cases)}] "
            f"{case['id']}: {case['question']}"
        )

        record = {
            "id": case["id"],
            "category": case["category"],
            "question": case["question"],
            "expected_intent": case["expected_intent"],
            "expected_status": case["expected_status"],
            "requires_sources": case["requires_sources"],
            "actual_intent": None,
            "actual_status": None,
            "answer": "",
            "sources": [],
            "ticket_id": None,
            "intent_correct": None,
            "status_correct": None,
            "source_check": None,
            "answer_correctness": "needs_manual_review",
            "unsupported_claims": "needs_manual_review",
            "error": None
        }

        try:

            thread_id = str(uuid.uuid4())

            with patch(
                "agents.customerSupportAgent.FindOrCreateSupportTicket",
                side_effect=MockCreateTicket
            ), patch(
                "agents.customerSupportAgent.NotifySupportWebhook",
                side_effect=MockNotification
            ):

                response = RunCustomerSupportAgent(
                    question=case["question"],
                    thread_id=thread_id
                )

            record["actual_intent"] = response.get("intent")
            record["actual_status"] = response.get("status")
            record["answer"] = str(
                response.get("answer", "")
            )

            sources = response.get("sources") or []

            record["sources"] = sources
            record["ticket_id"] = response.get("ticket_id")

            if case["expected_intent"] is not None:
                record["intent_correct"] = (
                    record["actual_intent"]
                    == case["expected_intent"]
                )

            if case["expected_status"] is not None:
                record["status_correct"] = (
                    record["actual_status"]
                    == case["expected_status"]
                )

            if case["requires_sources"]:
                record["source_check"] = bool(sources)

            print(
                "  Intent:",
                record["actual_intent"],
                "| Status:",
                record["actual_status"]
            )

        except Exception as error:

            record["error"] = (
                f"{type(error).__name__}: {error}"
            )

            print("  ERROR:", record["error"])

        results.append(record)

    
    def Score(field):

        eligible = [
            row
            for row in results
            if (
                field != "intent_correct"
                or row["expected_intent"] is not None
            )
            and (
                field != "status_correct"
                or row["expected_status"] is not None
            )
            and (
                field != "source_check"
                or row["requires_sources"]
            )
        ]

        evaluated = len(eligible)

        passed = sum(
            row["error"] is None
            and row[field] is True
            for row in eligible
        )

        return {
            "passed": passed,
            "evaluated": evaluated,
            "percentage": (
                round(passed / evaluated * 100, 2)
                if evaluated
                else None
            )
        }

    summary = {
        "total_cases": len(results),
        "completed_cases": sum(
            row["error"] is None
            for row in results
        ),
        "intent_accuracy": Score("intent_correct"),
        "outcome_accuracy": Score("status_correct"),
        "source_coverage": Score("source_check"),
        "answer_correctness": "pending_manual_review",
        "unsupported_claims": "pending_manual_review"
    }

    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%d_%H%M%S")

    json_path = RESULTS_DIR / f"evaluation_{timestamp}.json"
    csv_path = RESULTS_DIR / f"evaluation_{timestamp}.csv"

    json_path.write_text(
        json.dumps(
            {
                "summary": summary,
                "cases": results
            },
            indent=2,
            ensure_ascii=False,
            default=str
        ),
        encoding="utf-8"
    )

    fields = [
        "id",
        "category",
        "question",
        "expected_intent",
        "actual_intent",
        "intent_correct",
        "expected_status",
        "actual_status",
        "status_correct",
        "source_check",
        "answer_correctness",
        "unsupported_claims",
        "answer",
        "sources",
        "ticket_id",
        "error"
    ]

    with csv_path.open(
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fields
        )

        writer.writeheader()

        for row in results:
            writer.writerow({
                key: (
                    json.dumps(row[key], default=str)
                    if key == "sources"
                    else row[key]
                )
                for key in fields
            })

    print("\n========== EVALUATION SUMMARY ==========")

    for name in [
        "intent_accuracy",
        "outcome_accuracy",
        "source_coverage"
    ]:

        metric = summary[name]

        print(
            f"{name}: "
            f"{metric['passed']}/{metric['evaluated']} "
            f"({metric['percentage']}%)"
        )

    print(
        "Answer correctness: pending manual review"
    )

    print(
        "Unsupported claims: pending manual review"
    )

    print("\nJSON:", json_path)
    print("CSV:", csv_path)

    return summary


if __name__ == "__main__":
    RunEvaluation()
