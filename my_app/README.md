# LifePIM Sample App

This folder is a starter app that loads LifePIM AI Core using a user-editable
configuration file.

## How it works

`lifepim_config.py` is loaded automatically (if present) and overrides the
defaults from `src/lifepim_ai_core/core/llm_runtime/defaults.py`.

## Quick start

1. Edit `lifepim_config.py` to point at your documents and desired model.
2. Build/rebuild your vectorstore if needed.
3. Run the sample CLI:

```bash
python my_app/main.py "hello - who are you?"
```
