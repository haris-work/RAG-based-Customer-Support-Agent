
import copy
import tempfile

from pathlib import Path
from unittest.mock import patch

from scripts.checkEvaluationRegression import (
    SetBaseline,
    CheckRegression
)

import json


def BuildEvaluation(intent_pass=True):

    case = {
        "id": "REG001",
        "category": "human_escalation",
        "question": "Connect me with human support.",
        "expected_intent": "human_support",
        "expected_status": "needs_review",
        "requires_sources": False,
        "intent_correct": intent_pass,
        "status_correct": True,
        "source_check": None,
        "error": None
    }

    passed = 1 if intent_pass else 0

    return {
        "summary": {
            "total_cases": 1,
            "completed_cases": 1,
            "intent_accuracy": {
                "passed": passed,
                "evaluated": 1,
                "percentage": float(passed * 100)
            },
            "outcome_accuracy": {
                "passed": 1,
                "evaluated": 1,
                "percentage": 100.0
            },
            "source_coverage": {
                "passed": 0,
                "evaluated": 0,
                "percentage": None
            }
        },
        "cases": [case]
    }


def TestEvaluationRegression():

    with tempfile.TemporaryDirectory() as folder:

        folder = Path(folder)

        baseline_file = folder / "baseline.json"
        result_file = folder / "evaluation.json"

        with patch(
            "scripts.checkEvaluationRegression.BASELINE_PATH",
            baseline_file
        ):

            print("\nTEST 1: Establish baseline")

            result_file.write_text(
                json.dumps(BuildEvaluation(True)),
                encoding="utf-8"
            )

            SetBaseline(result_file)

            assert baseline_file.exists()

            print("PASS: Baseline saved")

            print("\nTEST 2: Identical results")

            assert CheckRegression(result_file) is True

            print("PASS: No regression")

            print("\nTEST 3: Reduced intent accuracy")

            result_file.write_text(
                json.dumps(BuildEvaluation(False)),
                encoding="utf-8"
            )

            assert CheckRegression(result_file) is False

            print("PASS: Regression detected")

            print("\nTEST 4: Changed evaluation dataset")

            changed = copy.deepcopy(BuildEvaluation(True))

            changed["cases"][0]["question"] = (
                "A different customer question"
            )

            result_file.write_text(
                json.dumps(changed),
                encoding="utf-8"
            )

            try:
                CheckRegression(result_file)

            except ValueError:
                print("PASS: Dataset change rejected")

            else:
                raise AssertionError(
                    "Changed evaluation dataset was accepted"
                )

    print("\nALL REGRESSION TESTS PASSED")


if __name__ == "__main__":
    TestEvaluationRegression()
