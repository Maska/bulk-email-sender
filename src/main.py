"""Entrypoint to the app. Run this file with Python."""

import csv
import logging
from pathlib import Path

import emailer
import letter
from config import read_config

LOG = logging.getLogger(__name__)

ROOT_PATH = Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = ROOT_PATH / "default_config.toml"
CONFIG_PATH = ROOT_PATH / "config.toml"


def main() -> None:
    """Tie business logic together."""
    if (config := read_config(CONFIG_PATH)) is None:
        LOG.info("Using the default configs.")
        if (config := read_config(DEFAULT_CONFIG_PATH)) is None:
            LOG.error("No config files found, exiting")
            return
    _set_up_logging(config)

    entries = _read_csv(config["paths"]["input_csv"])
    letter.create_letters(entries, config)
    if config["modus_operandi"] == "actually send all emails":
        emailer.send_messages(entries, config)
    else:
        LOG.info("Running in test mode. Not sending email")


def _set_up_logging(config: dict) -> None:
    """Set up logging format and level."""
    kwargs = {
        "format": "%(asctime)s %(module)s %(levelname)s %(message)s",
        "datefmt": "%Y-%m-%dT%H:%M:%SZ",
        "level": config["logging_level"],
    }
    logging.basicConfig(**kwargs)
    LOG.info(f"Set logging level to {config['logging_level']}")


def _read_csv(path: str) -> list[dict]:
    """Read the CSV at path and return a list of all its entires."""
    LOG.debug(f"Reading personalization entries from {path}")
    path = Path(path)
    with path.open("r", newline="") as file:
        return list(csv.DictReader(file, delimiter=","))


if __name__ == "__main__":
    main()
