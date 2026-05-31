"""Tools to parse CSV with entries and represent one entry."""

import logging
import tomllib
from copy import deepcopy
from pathlib import Path

LOG = logging.getLogger(__name__)
ROOT_PATH = Path(__file__).parent.parent


def read_config(path: Path) -> dict | None:
    """Read config from a file and return it as a dict."""
    try:
        with path.open("rb") as file:
            return tomllib.load(file)
    except (tomllib.TOMLDecodeError, OSError) as e:
        LOG.warning(f"Failed to load config from {path}: {e}")


def personalize(config: dict, entry: dict) -> dict:
    """Return a deep copy of config with all string fields personalized."""
    personal = deepcopy(config)
    # First convert path strs to Paths, so they're skipped when recursing.
    if personal.get("paths"):
        for path_name, path_text in personal["paths"].items():
            personalized_path_text = path_text.format(**entry)

            path = Path(personalized_path_text)
            if not path.is_absolute():
                path = ROOT_PATH / personalized_path_text
            personal["paths"][path_name] = path

    def recurse_dict(parent: dict) -> None:
        for child_key, child_val in parent.items():
            if isinstance(child_val, str):
                parent[child_key] = child_val.format(**entry)
            elif isinstance(child_val, dict):
                recurse_dict(child_val)
            elif isinstance(child_val, list):
                # Thus far the only arrays we have are [[arrays_of_tables]].
                for dict_in_list in child_val:
                    recurse_dict(dict_in_list)

    recurse_dict(personal)
    return personal
