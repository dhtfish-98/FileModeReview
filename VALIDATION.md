# Validation record

Scope: World-writable regular files and group/other permissions on sensitive-name files.

Local checks to rerun:

```sh
python -m unittest discover -s tests -v
python cli.py --help
python -m compileall -q review.py cli.py tests
```

Check the exact public GitHub commit and its workflow run separately after publishing. Tests use synthetic input; no production system or external target is exercised. POSIX modes alone do not cover ACLs, ownership, encryption, open handles or effective access; concurrent changes are not controlled.

## Current source result (2026-10-02)

- Python 3.14.6: 5/5 unit and CLI integration tests passed.
- Tests include the specific malformed-input, incomplete-review and declaration cases added during the source audit.
- Directory traversal errors propagate to the CLI. .env variants are included in sensitive-name prompts. Findings describe permission bits; effective access still depends on ownership, ACLs and filesystem state.
- Test input is synthetic. No external target, live credential or production cluster is exercised.
- The public commit and its corresponding GitHub workflow must be verified separately after this update.
