# AI Evaluation and Regression Testing

## Status

The evaluation framework and baseline checker were implemented as part of **Steps 5.19–5.20**. This document does **not** assert a particular accuracy value because no evaluation result file was provided for independent verification.

## Dataset

`evaluations/supportEvaluationCases.json` contains representative fictional customer-support requests with expected intent (where labeled), expected answer-vs-escalation outcome, and whether source citations are required.

The initial case set was deliberately small. Labels should be reviewed against the actual 18 Markdown knowledge-base documents before the scores are interpreted as model quality.

## Run the agent evaluation

```powershell
python -m scripts.runAgentEvaluation
```

The runner uses fresh conversation IDs to reduce cross-case contamination. Groq inference and retrieval are real, so network access and API credentials are required. Ticket creation and outbound notification calls are mocked in the evaluation workflow as designed.

The runner writes JSON and CSV results to `evaluations/results/`.

## Automated metrics

- **Intent accuracy:** correct labels divided by cases with an expected intent.
- **Outcome accuracy:** correct `answered` vs `needs_review` decisions among labeled cases.
- **Citation coverage:** answered policy cases that include required citations.

Execution errors must count against the expected-case denominator rather than disappearing from the score. An explicit lack of expectation is not scored.

## Manual review

The following cannot be inferred from citations or routing accuracy alone:

- Factual correctness against the actual company policy.
- Whether a citation supports a specific statement.
- False claims about tracking, refunds, returns or account actions.
- Whether uncertainty is acknowledged appropriately.
- Whether escalation was necessary in context.

Keep manually reviewed labels separate from automated scores unless the aggregation logic explicitly includes those labels.

## Regression checker

After a validated evaluation completes:

```powershell
python -m scripts.checkEvaluationRegression --set-baseline
```

Subsequent runs:

```powershell
python -m scripts.runAgentEvaluation
python -m scripts.checkEvaluationRegression --check
```

The checker compares the same dataset and flags decreases in evaluated pass counts. It also rejects changes in labels/questions without establishing a new baseline. It is not a substitute for statistical testing: a small set of generative LLM calls may vary from run to run.

## Results reporting template

| Metric | Verified score | Dataset | Date |
| --- | --- | --- | --- |
| Intent classification | Pending actual result | Initial labeled set | — |
| Expected routing outcome | Pending actual result | Initial labeled set | — |
| Required source citation coverage | Pending actual result | Initial labeled set | — |
| Factual answer correctness | Pending manual review | KB-grounded cases | — |
| Unsupported factual/action claims | Pending manual review | KB-grounded cases | — |

## Baseline integrity

Keep a reviewed baseline file with code revisions. Do not overwrite a baseline merely to make a regression test pass. Keep raw reports private if they include unreviewed text, internal paths or any non-fictional data.
