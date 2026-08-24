## ADDED Requirements

### Requirement: The mirror `LangfusePromptResolver` class

The system SHALL provide a `LangfusePromptResolver` class at `baml_src/_shared/langfuse_prompt_resolver.py` with the SAME circuit-breaker + graceful-fallback pattern as cianchosaint + 15 ciandlithe-specific canonical prompt names.

#### Scenario: The ciandlithe resolver has 15 canonical prompt names

- **WHEN** the operator runs `LangfusePromptResolver.canonical_prompt_names()` in ciandlithe
- **THEN** the result SHALL include exactly the 15 names listed in §Purpose

#### Scenario: The mirror resolver falls back to inline BAML prompts

- **WHEN** Langfuse is unconfigured
- **THEN** the resolver SHALL return a `LangfusePromptHit` with `fallback_used=True`

#### Scenario: The mirror resolver opens the circuit-breaker after 3 consecutive failures

- **WHEN** the resolver records 3 consecutive failures
- **THEN** the circuit-breaker SHALL transition to `is_open=True`

### Requirement: Cross-repo sync with cianchosaint

The system SHALL be the **mirror** of the cianchosaint `cianchosaint-langfuse-prompt-management` spec.

#### Scenario: The ciandlithe resolver shares the same circuit-breaker constants

- **WHEN** the operator inspects `langfuse_prompt_resolver.py` in ciandlithe
- **THEN** the `CIRCUIT_BREAKER_THRESHOLD` SHALL be 3
- **AND** the `CIRCUIT_BREAKER_RESET_SECONDS` SHALL be 60

#### Scenario: The ciandlithe resolver has different LANGFUSE_HOST

- **WHEN** the operator inspects the default `LANGFUSE_HOST`
- **THEN** it SHALL be `https://langfuse.ciandlithe.ie`