# PR Stack Template

PR description should include these fields:

<<<<<<< HEAD
<<<<<<< HEAD
- Depends-on: `PR-1-id | none`
- Stack-Layer: L1 | L2 | L3 | L4 (maps to capabilities, work packages, tasks, deliverables)
- Release-Channel: alpha | beta | rc | canary | release
- State: optional override when lifecycle differs from release channel
- Rollback-Plan: `command or rollback branch`
=======
- Depends-on: <PR-1-id | none>
- Stack-Layer: L1 | L2 | L3 | L4 (maps to capabilities, work packages, tasks, deliverables)
- Release-Channel: alpha | beta | rc | canary | release
- State: if different from release channel, explicitly explain variance.
- Rollback-Plan: <command or rollback branch>
>>>>>>> 53244ab (docs: address review comments for stacked PR handbook)
=======
- Depends-on: `PR-1-id | none`
- Stack-Layer: L1 | L2 | L3 | L4 (maps to capabilities, work packages, tasks, deliverables)
- Release-Channel: alpha | beta | rc | canary | release
- State: if different from release channel, explicitly explain variance.
- Rollback-Plan: `command or rollback branch`
>>>>>>> 44c6b82 (docs: stabilize PR docs build for CI gates)
- Compatibility: BREAKING | NON_BREAKING
- API-Shape-Impact: none | additive | breaking
- Validation: lint, test, migration check with command list

If API-Shape-Impact is `breaking`:
- child PRs that compile against this API cannot merge first.
