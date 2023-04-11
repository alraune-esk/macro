import os, sys
import importlib
from abc import abstractmethod
from pathlib import Path

class Macro(object):

    @classmethod
    @abstractmethod
    def macro_run(mode:str):

        raise NotImplementedError

EXCLUDED_PREFIXES = ("-", "_")
PY_FILE_EXT = (".py", ".pyc")

FILE_ROOT = Path(__file__).parent
MACRO_REGISTRY = []


def register_macro(macro):
    MACRO_REGISTRY.append(macro)

    if macro in MACRO_REGISTRY:
        raise ValueError(f'Cannot register duplicate Macro ({macro})')
    

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


macro_filenames = sorted(
    f for f in os.listdir(FILE_ROOT)
    if f.endswith(PY_FILE_EXT) and not f.startswith(EXCLUDED_PREFIXES)
)

for file in macro_filenames:
    module_name = f'{os.path.splitext(os.path.basename(file))[0]}'
    if module_name not in sys.modules:
        importlib.import_module(module_name)



