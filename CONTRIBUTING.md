# Contributing to GUIpi26

Thanks for considering a contribution. GUIpi26 is in **alpha** — APIs are still moving, so check open issues and discussions before sinking time into a large change.

## Local setup

```powershell
git clone https://github.com/DillanStep/guipi26
cd guipi26
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

Verify it works:

```powershell
python examples\dashboard.py
```

## Branching model

- **`main`** — release branch. Only updated by merging `develop` (or hotfix branches) when cutting a release. Tags (`v*`) are created here and trigger the PyPI publish workflow.
- **`develop`** — integration branch. Day-to-day work merges here.
- **feature branches** — branch from `develop` using `feat/short-description`, `fix/short-description`, or `docs/short-description`. Open PRs into `develop`.

## Workflow

1. Open (or comment on) an issue describing what you want to change.
2. Branch from `develop`: `git checkout develop && git pull && git checkout -b feat/short-description`.
3. Keep the change focused — small PRs land faster.
4. Run the smoke checks before pushing:
   ```powershell
   python -m build
   python -m twine check dist/*
   python examples\dashboard.py
   python examples\contacts\app.py
   python benchmarks\run_all.py --controls 100 --paints 40 --runs 1
   ```
5. Update [docs](docs/) if you changed the public API.
6. Open a PR using the template.

## Code style

- Pure stdlib + `ctypes`. No third-party runtime dependencies.
- Windows-only is fine — don't add cross-platform shims that aren't needed.
- Keep the public API surface in [guipi26/__init__.py](guipi26/__init__.py) explicit.
- Match the existing function signature style: keyword-only after `x, y, width, height`.

## Reporting bugs

Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.yml). Always include a minimal reproduction.

## License

By contributing, you agree your code is released under the [MIT license](LICENSE).
