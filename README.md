# Bulk email sender with personalized PDF attachments

Create and send personalized email with attachments.

This document describes how the system functions,
gives usage instructions
and documents how to set up a development environment.
The instructions are intended for also novice users to follow.

The system reads recipient data from a CSV file and,
for each line,
stamps a template with personalized texts,
creates a PDF file
and sends it to the designated recipient by email.


## Usage instructions

The commands in these instructions assume you are using a command line
and have changed directory to the same folder where this file is located.

Also it is assumed that you use Gmail.
If you use another email provider, no problem.
The system needs all the same info as you'd need when setting up an email app on your machine.

Here's everything simplified:
1. Install Python and test run the app
1. Add an App Password to your email account
1. Update email sending configuration and test
1. Create a template PDF
1. Replace test data with real data and run the system
1. Remove the App Password from your email account

### Python

The system is run with a Python interpreter.
You can get it for Windows and other operating systems.
You need at least Python version 3.11 to run the system.
The latest version is usually the best choice to install.

[Install](https://docs.astral.sh/uv/getting-started/installation/)
the package manager `uv`.
Then use it to install the latest Python version and test run the app:

    uv python install
    uv run src/main.py

Check that PDF letters were created in the *output* folder.
You don't have to worry about any email being sent,
as that's only later enabled in the configuration.

### Email App Password

To use your email account (e.g. Gmail) through an external app such as this,
create an App Password.
This bypasses multi-factor authentication
and doesn't require you to use your account's main password here.

See [Google's instructions](https://support.google.com/mail/answer/185833?hl=fi).
Remember to remove the password after use.

### Configuration file

Create *config.toml* as a copy of *default_config.toml*.
Set the following fields:
 - Your email address
 - Pretty sender name ("First Last <address>")
 - App password
 - Subject line of the email message
 - Body text of the email message (avoid lines longer than 70 characters)
 - Set the operation mode to actually send email

You can also make other changes as you see fit.
There are more instructions in the config file.
Test the config with the same test CSV file by running the system

    uv run src/main.py

and checking from your actual email appliction's user interface,
in the sent folder,
that the messages are there.
Especially check that the sender names and attachments are correct.
Check also the inboxes of your email addresses that you configured in the CSV.
The messages should have come through.

### Create a template PDF

Export your letter as a PDF,
adjust the configuration to use that as a template
and position new lines of text as needed.
It will take some iteration to accurately position the texts.

You will likely want to copy the font you used for your letter
into the fonts folder and use that for the text.

### Import real data

Export your data as a CSV.
Make sure the fields are comma-separated like in the example file.
Adjust the configuration to use your CSV.

You might want to temporarily enable test mode in the config again
to make sure letter creation works works with real data as well.
After testing, run without test mode

    uv run src/main.py

and check your sent folder to verify the messages were sent.
It will take a minute or two to send a few dozen emails with attachments.
Don't touch the command line while the system is running.

### Remove the email App Password

Do remember to remove it.
For Gmail, you can do it from the same page where you added it.


## Setting up a development environment

Actually just perform the same steps as in the instructions above.
For development, we have `ruff` to lint and format the code.
No tests exist yet.
