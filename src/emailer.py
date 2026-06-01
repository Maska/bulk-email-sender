"""Send emails."""

import functools
import logging
import mimetypes
import smtplib
from collections.abc import Callable
from email.message import EmailMessage
from pathlib import Path

from config import personalize

LOG = logging.getLogger(__name__)


def send_messages(entries: list[dict], config: dict) -> None:
    """Send the messages over one connection."""
    LOG.info(f"Sending {len(entries)} messages")
    send_all_messages = functools.partial(_send_messages, entries, config)
    _while_logged_in(send_all_messages, config["email"]["server"])
    LOG.info("All emails sent")


def _while_logged_in(send_func: Callable, config: dict) -> None:
    """Log into an email server. Call the send func with the server as arg."""
    LOG.info(f"Connecting to {config['address']}:{config['port']}")
    with smtplib.SMTP_SSL(config["address"], config["port"]) as server:
        LOG.info(f"Logging in as {config['account']}")
        server.login(config["account"], config["password"])
        send_func(server)


def _send_messages(
    entries: list[dict],
    config: dict,
    server: smtplib.SMTP,
) -> None:
    """While logged in to server, create and send messages for all entries."""
    for entry in entries:
        personal_config = personalize(config, entry)
        to = personal_config["email"]["message"]["to"]

        LOG.debug(f"Sending an email to {to}")
        server.send_message(_create_message(personal_config))
        LOG.info(f"Sent an email to {to}")


def _create_message(config: dict) -> EmailMessage:
    """Create an email message with an attached file to the recipient."""
    msg_cfg = config["email"]["message"]
    LOG.debug(f"Creating an email: {msg_cfg}")

    msg = EmailMessage()
    msg["Subject"] = msg_cfg["subject"]
    msg["From"] = msg_cfg["from"]
    msg["To"] = msg_cfg["to"]
    if cc := msg_cfg["cc"]:
        msg["Cc"] = cc.replace(";", ",")

    msg.set_content(msg_cfg["body"])
    if body_html := msg_cfg["body_html"]:
        msg.add_alternative(body_html, subtype="html")

    if (path := config["paths"]["attachment"]) and path.is_file():
        _attach_file(msg, path)
    return msg


def _attach_file(msg: EmailMessage, path: Path) -> None:
    """Attach the file at the path to the email message."""
    LOG.debug(f"Attaching {path} to email")
    content_type, compression_encoding = mimetypes.guess_type(path)
    if content_type is None or compression_encoding is not None:
        content_type = "application/octet-stream"
    main_type, sub_type = content_type.split("/", 1)
    with path.open("rb") as file:
        msg.add_attachment(
            file.read(),
            maintype=main_type,
            subtype=sub_type,
            filename=path.name,
        )
