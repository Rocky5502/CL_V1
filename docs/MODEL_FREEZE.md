# Model freeze protocol

Before a confirmatory run, resolve and record the exact checkpoint revision for every local model and the exact provider model identifier for every hosted model. Also record tokenizer/processor revision, loader class, precision, generation settings, chat-template settings, SDK/library versions, and run date.

Use `python scripts/freeze_models.py` and `python scripts/freeze_environment.py` after the local smoke tests pass. If any provider alias or checkpoint changes later, treat it as a new experimental condition rather than silently replacing the frozen model.
