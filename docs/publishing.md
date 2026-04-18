# Publishing

GUIpi26 is built with [hatchling](https://hatch.pypa.io/) and ships to PyPI like any other Python package. Today it's published as an **alpha pre-release** so users have to opt in.

## Pre-release versioning (PEP 440)

PyPI and `pip` understand pre-release suffixes natively. Pick one for the current release:

| Suffix | Example | When to use |
| --- | --- | --- |
| `.devN` | `0.1.0.dev0` | Internal/dev snapshots, "anything goes" |
| `aN` | `0.1.0a1` | Alpha \u2014 early preview, APIs will change |
| `bN` | `0.1.0b1` | Beta \u2014 feature-complete preview |
| `rcN` | `0.1.0rc1` | Release candidate |
| _(none)_ | `0.1.0` | Stable release |

`pip install guipi26` **skips pre-releases by default**. Users get a pre-release only with `pip install --pre guipi26` (or by pinning an exact version, e.g. `guipi26==0.1.0a1`). That's exactly the "preview, opt in" signal we want during early development.

GUIpi26 currently ships as `0.1.0a1` and the `Development Status :: 3 - Alpha` classifier reinforces this on the PyPI page.

## Build

From the project root:

```
python -m pip install --upgrade build twine
python -m build
```

Produces:

```
dist/guipi26-0.1.0a1-py3-none-any.whl
dist/guipi26-0.1.0a1.tar.gz
```

## Verify

```
python -m twine check dist/*
```

Both artifacts should report `PASSED`.

## Upload to TestPyPI first (recommended for previews)

```
python -m twine upload --repository testpypi dist/*
```

Install from TestPyPI with `--pre` to mimic what real users will do:

```
pip install --pre --index-url https://test.pypi.org/simple/ guipi26
```

## Upload to real PyPI

```
python -m twine upload dist/*
```

After upload, users install with:

```
pip install --pre guipi26
```

The PyPI page will show a "pre-release" badge, and the alpha classifier makes the warning visible.

## Bumping the preview version

Two files hold the version:

1. `pyproject.toml` \u2014 `[project] version = "..."`
2. `guipi26/__init__.py` \u2014 `__version__ = "..."`

Increment the alpha number for each preview cut:

```
0.1.0a1 -> 0.1.0a2 -> 0.1.0a3 -> ... -> 0.1.0b1 -> 0.1.0rc1 -> 0.1.0
```

Each version number on PyPI is **immutable** \u2014 you can't re-upload `0.1.0a1` after a fix. Bump and upload again.

## Graduating from alpha

When the API stops moving:

1. Update both version strings to drop the suffix (e.g. `0.1.0`).
2. Change the classifier in `pyproject.toml` from `Development Status :: 3 - Alpha` to `Development Status :: 4 - Beta` (or `5 - Production/Stable`).
3. Remove the early-preview banner and the `--pre` install instruction from `README.md`.
4. Build, check, upload.

## Release checklist

1. Bump version in `pyproject.toml` and `guipi26/__init__.py`.
2. `Remove-Item dist/* -Recurse -Force` (or `rm -rf dist/`).
3. `python -m build`
4. `python -m twine check dist/*`
5. (Optional) Upload to TestPyPI and try `pip install --pre`.
6. `python -m twine upload dist/*`
7. Tag the commit: `git tag v0.1.0a1 && git push --tags`.

## Yanking a bad preview

If a preview release has a serious bug, **yank** it on PyPI (Manage \u2192 Releases \u2192 Yank). Yanked versions stay installable for anyone who pinned them but won't be picked up by fresh `pip install --pre` runs. Then ship a new alpha with the fix.
