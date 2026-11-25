
import argparse
import json
import sys

from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

RESULTS_DIR = BASE_DIR / "evaluations" / "results"

BASELINE_PATH = (
    BASE_DIR / "evaluations" / "baseline.json"
)

METRICS = [
    "intent_accuracy",
    "outcome_accuracy",
    "source_coverage"
]


def LoadEvaluation(path):

    with Path(path).open(
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Invalid evaluation document")

    if "summary" not in data or "cases" not in data:
        raise ValueError("Missing evaluation fields")

    return data


def GetLatestEvaluation():

    files = sorted(
        RESULTS_DIR.glob("evaluation_*.json"),
        key=lambda path: path.stat().st_mtime
    )

    if not files:
        raise FileNotFoundError(
            "No evaluation results found. "
            "Run scripts.runAgentEvaluation first."
        )

    return files[-1]


def ValidateEvaluation(data):

    cases = data["cases"]

    if not isinstance(cases, list) or not cases:
        raise ValueError("Evaluation cases are empty")

    ids = [case["id"] for case in cases]

    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate evaluation case IDs")

    summary = data["summary"]

    if summary["total_cases"] != len(cases):
        raise ValueError("Incorrect total case count")

    if summary["completed_cases"] != sum(
        case.get("error") is None
        for case in cases
    ):
        raise ValueError("Incorrect completed case count")

    for field in METRICS:

        metric = summary[field]

        if not isinstance(metric["passed"], int):
            raise ValueError(f"Invalid metric: {field}")

        if not isinstance(metric["evaluated"], int):
            raise ValueError(f"Invalid metric: {field}")

        expected_count = sum(
            field != "intent_accuracy"
            or case["expected_intent"] is not None
            for case in cases
        ) if field == "intent_accuracy" else sum(
            field != "outcome_accuracy"
            or case["expected_status"] is not None
            for case in cases
        ) if field == "outcome_accuracy" else sum(
            bool(case["requires_sources"])
            for case in cases
        )

        if metric["evaluated"] != expected_count:
            raise ValueError(
                f"Incorrect denominator for {field}. "
                "Rerun the corrected evaluation script."
            )

        actual_passed = sum(
            case.get("error") is None
            and case.get({
                "intent_accuracy": "intent_correct",
                "outcome_accuracy": "status_correct",
                "source_coverage": "source_check"
            }[field]) is True
            for case in cases
        )

        if metric["passed"] != actual_passed:
            raise ValueError(
                f"Incorrect passed count for {field}"
            )

        count = metric["evaluated"]

        if count == 0:
            if metric["percentage"] is not None:
                raise ValueError("Invalid empty metric")
        else:
            expected_percentage = round(
                metric["passed"] / count * 100,
                2
            )

            if metric["percentage"] != expected_percentage:
                raise ValueError(
                    f"Incorrect percentage for {field}"
                )


def CaseSignature(case):

    return (
        case["question"],
        case["category"],
        case["expected_intent"],
        case["expected_status"],
        case["requires_sources"]
    )


def SetBaseline(path):

    data = LoadEvaluation(path)

    ValidateEvaluation(data)

    if data["summary"]["completed_cases"] != len(
        data["cases"]
    ):
        raise ValueError(
            "Cannot establish baseline: "
            "one or more evaluation cases failed to execute"
        )

    baseline = {
        "created_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "source_file": Path(path).name,
        "evaluation": data
    }

    BASELINE_PATH.write_text(
        json.dumps(
            baseline,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    print("Baseline established:", BASELINE_PATH)

    for field in METRICS:
        metric = data["summary"][field]

        print(
            f"{field}: "
            f"{metric['passed']}/{metric['evaluated']} "
            f"({metric['percentage']}%)"
        )


def CheckRegression(path):

    if not BASELINE_PATH.exists():
        raise FileNotFoundError(
            "Baseline not found. "
            "Run --set-baseline first."
        )

    baseline = json.loads(
        BASELINE_PATH.read_text(encoding="utf-8")
    )["evaluation"]

    current = LoadEvaluation(path)

    ValidateEvaluation(baseline)
    ValidateEvaluation(current)

    baseline_cases = {
        case["id"]: CaseSignature(case)
        for case in baseline["cases"]
    }

    current_cases = {
        case["id"]: CaseSignature(case)
        for case in current["cases"]
    }

    if baseline_cases != current_cases:
        raise ValueError(
            "Evaluation dataset changed. "
            "Use the same labeled cases before comparing."
        )

    failures = []

    if current["summary"]["completed_cases"] != len(
        current["cases"]
    ):
        failures.append("One or more evaluation cases failed")

    print("\nREGRESSION REPORT")
    print("-" * 58)

    for field in METRICS:

        previous = baseline["summary"][field]
        latest = current["summary"][field]

        if previous["evaluated"] != latest["evaluated"]:
            raise ValueError(
                f"Metric denominator changed: {field}"
            )

        old_score = previous["passed"]
        new_score = latest["passed"]

        print(
            f"{field}: "
            f"{old_score}/{previous['evaluated']} "
            f"-> {new_score}/{latest['evaluated']}"
        )

        if new_score < old_score:
            failures.append(field)

    print("-" * 58)

    if failures:

        print("REGRESSION CHECK: FAIL")

        for failure in failures:
            print(" -", failure)

        return False

    print("REGRESSION CHECK: PASS")
    print("No measured regression detected")

    return True


def Main():

    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(
        required=True
    )

    group.add_argument(
        "--set-baseline",
        action="store_true"
    )

    group.add_argument(
        "--check",
        action="store_true"
    )

    parser.add_argument(
        "--file",
        type=Path,
        default=None
    )

    args = parser.parse_args()

    path = args.file or GetLatestEvaluation()

    if args.set_baseline:
        SetBaseline(path)
        return 0

    return 0 if CheckRegression(path) else 1


if __name__ == "__main__":

    try:
        sys.exit(Main())

    except (
        OSError,
        ValueError,
        KeyError,
        TypeError
    ) as error:

        print("Evaluation error:", error)
        sys.exit(2)
