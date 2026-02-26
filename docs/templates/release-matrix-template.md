# Release Matrix Template

Date: YYYY-MM-DD
Program: <name>
Channel: alpha|beta|rc|canary|release

| Task ID | Parent ID | PR Name | State | Depends On | Risks | Gate Result | Owner | Rollback | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | - | feat/...-alpha-core | alpha | - | low | pass | <owner> | none | foundation |
| 1.1 | 1 | feat/...-beta-cache | beta | 1 | med | pass | <owner> | git revert <sha> | perf cache |
| 1.2 | 1 | feat/...-rc-renderer | rc | 1 | high | pass | <owner> | revert to legacy renderer | gated rollout |
