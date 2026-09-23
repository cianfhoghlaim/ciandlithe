# remove-students-union-from-ciandlithe Specification

## Purpose
TBD - created by archiving change 2026-09-23-remove-students-union-from-ciandlithe-v1. Update Purpose after archive.

## Requirements

### Requirement: ciandlithe owns only BLIP v1 (civil-litigation) content
The system SHALL restrict ciandlithe to the British Isles civil-litigation OSINT platform (BLIP v1) per `ciandlithe/README.md:5`. Non-civil-litigation content (e.g. the SU case studies) belongs in cianfhoghlaim.

#### Scenario: ciandlithe's SU package is deleted
- **WHEN** the operator archives `openspec/changes/2026-09-23-remove-students-union-from-ciandlithe-v1/`
- **THEN** `ls ciandlithe/agents/adk/students_union/` fails (dir removed)
- **AND** `git grep students_union` in ciandlithe returns 0 (except in updated README/AGENTS/LICENSE pointers)

### Requirement: The ciandlithe-adk-students-union spec is deleted
The system SHALL delete `openspec/specs/ciandlithe-adk-students-union/spec.md` (the SU capability spec). The content absorbs into cianfhoghlaim's `cianfhoghlaim-tertiary-pipeline` spec as the "Students' Union case studies" Requirement.

#### Scenario: ciandlithe-adk-students-union spec is deleted
- **WHEN** the operator archives this change
- **THEN** `ls openspec/specs/ciandlithe-adk-students-union/` fails (dir removed)
