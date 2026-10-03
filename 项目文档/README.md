> 目录已整理：文档在「项目文档」，构建、缓存与暂存输入在「Build」。从仓库根目录运行 `python3 构建.py --build`；如需使用本文原有源码命令，先运行 `python3 构建.py --stage --ci`，再进入 `Build/源码`。暂存会恢复原输入路径。现有版本和历史验证记录按各自提交理解。

# FileModeReview

Review selected permissions on a local directory tree without reading file contents. It runs locally, does not contact targets, and reports review prompts instead of exploit instructions.

## Input and checks

- Input: local directory from a system you own or are authorized to inspect.
- Checks: World-writable regular files and group/other permissions on sensitive-name files.
- Output: rule, local location and short note. No source snippets, credential values or log identities are printed.

## Run

```sh
python cli.py ./owned-tree
python cli.py ./owned-tree --json
python -m unittest discover -s tests -v
```

Exit code 0 means no findings, 1 means review findings, 2 means invalid input or read failure. A clean result is not a security guarantee. This tool examines file metadata in a local directory; it does not read file contents.

## Boundaries

POSIX modes alone do not cover ACLs, ownership, encryption, open handles or effective access; concurrent changes are not controlled. Work only on local, authorized inputs. The analysis does not send data to a service or modify the inspected files.

## Source and policy context

- Technical reference: https://docs.python.org/3/library/stat.html
- See [ORIGIN.md](<ORIGIN.md>) for implementation provenance and [VALIDATION.md](<VALIDATION.md>) for checks performed.
- CVP eligibility depends on a real, legitimate defensive task affected by Claude's cyber safeguards and the applicant's organization/identity review; this repository alone does not establish eligibility or approval. [Anthropic CVP guidance](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet).

## Reviewed input behavior

Directory traversal errors propagate to the CLI. .env variants are included in sensitive-name prompts. Findings describe permission bits; effective access still depends on ownership, ACLs and filesystem state.
