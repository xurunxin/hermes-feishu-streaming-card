import sys
import types

from . import cli_core as _core


class _CliProxy(types.ModuleType):
    def __getattr__(self, name: str):
        return getattr(_core, name)

    def __setattr__(self, name: str, value):
        if name in {"_core", "__class__"} or name.startswith("__"):
            return super().__setattr__(name, value)
        setattr(_core, name, value)

    def __dir__(self):
        return sorted(set(super().__dir__()) | set(vars(_core)))


_module = sys.modules[__name__]
_module.__class__ = _CliProxy
_module._core = _core
main = _core.main


if __name__ == "__main__":
    raise SystemExit(main())
