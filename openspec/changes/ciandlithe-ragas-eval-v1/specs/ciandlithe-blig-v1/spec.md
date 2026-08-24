## ADDED Requirements

### Requirement: The ciandlithe mirror RAGASEvaluator

The system SHALL provide a `CiandlitheRAGASEvaluator` class at `baml_src/_shared/ragas_evaluator.py`.

#### Scenario: Evaluates composite pilot RAGAS metrics

- **WHEN** the operator invokes `CiandlitheRAGASEvaluator().evaluate_composite_pilot(pilot_id, cohort, input_text, output_text)`
- **THEN** the method SHALL return a `CiandlitheRAGASExtractionScores` with the 5 RAGAS metrics

#### Scenario: Reports RAGAS scores to Langfuse

- **WHEN** the operator invokes `CiandlitheRAGASEvaluator().report_to_langfuse(scores, trace_id)`
- **THEN** the method SHALL call `report_ragas_scores()` (the ciandlithe-side helper)