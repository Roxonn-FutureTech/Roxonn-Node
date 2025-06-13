from __future__ import annotations

from exo.api.chatgpt_api import ChatGPTAPI as ChatGPTAPI

# --- Added shim to re-export the REST API server helpers from the sibling ``exo/api.py`` module.
# There is both a package named ``exo.api`` (this directory) and a standalone module file
# ``exo/api.py`` alongside it.  Python prefers the package over the module when importing
# ``exo.api``, which means symbols such as ``run`` that live in the module file are hidden.
# To preserve backward-compatibility (e.g. ``import exo.api as api`` in *exo/main.py*), we
# dynamically load the sibling file and re-export the relevant attributes here.

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

# Absolute path to the sibling ``api.py`` file (same parent directory as this package)
_api_file_path = Path(__file__).resolve().parent.parent / "api.py"

if _api_file_path.exists():
    spec = importlib.util.spec_from_file_location("_exo_api_file", _api_file_path)
    _api_module: ModuleType = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    assert spec and spec.loader  # for mypy/static checkers
    spec.loader.exec_module(_api_module)  # type: ignore[misc]

    # Re-export the public helpers expected by callers (e.g. ``run`` and mutable globals
    # used for configuration).
    for _name in ("run", "roxonn_wallet_address", "node_host", "node_port"):
        if hasattr(_api_module, _name):
            globals()[_name] = getattr(_api_module, _name)

    # Also register the module under ``exo._api_file`` so it can be imported directly if
    # desired without going through this shim.
    sys.modules.setdefault("exo._api_file", _api_module)

    # Make this package act as a transparent proxy for attributes of the loaded module so
    # that callers can freely read *and* mutate fields such as ``roxonn_wallet_address``.
    def __getattr__(attr):  # type: ignore[override]
        if attr in globals():
            return globals()[attr]
        return getattr(_api_module, attr)

    def __setattr__(attr, value):  # type: ignore[override]
        setattr(_api_module, attr, value)
        globals()[attr] = value

    # Inject the proxy functions into the module namespace.
    globals()["__getattr__"] = __getattr__
    globals()["__setattr__"] = __setattr__
else:
    # Fallback: provide a placeholder that raises a helpful error if accessed at runtime.
    def _missing(*_args, **_kwargs):  # type: ignore[return-type]
        raise AttributeError("The compiled API server implementation could not be located at" f" {_api_file_path}.")

    run = _missing  # type: ignore[assignment]
