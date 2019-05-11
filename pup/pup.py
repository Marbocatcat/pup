#!/usr/bin/python3.7

# 1. sudo dnf check-upgrade > upgrade_list.txt to be emailed to me.
# 2. sudo dnf upgrade -y if successfull send an email to me if not send an email with the error.
# 3. close program.


import subprocess
import logging
import smtplib
import sys
import os

from email.message import EmailMessage
from timestamp import timestamp
from pathlib import Path



# Logging Configurations
log_path = Path("/home/bobcat/pup_logs") / timestamp()
error_path = str(log_path) + ".log"
update_log = str(log_path) + ".txt"

logging.basicConfig(filename=error_path, level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')

# Email & Password
EMAIL = os.environ.get("EMAIL")
PASS = os.environ.get("G_PASS")


def install_update():

    okay = 0
    command = ["dnf", "upgrade", "-y"]
    installUpdate = subprocess.run(command, text=True, capture_output=True)

    logging.info("Installing updates")
    if installUpdate.returncode is not okay:
        logging.info(f"Error occured! Exit code: {installUpdate.returncode}")
        sys.exit(1)
    else:
        logging.info("Updates has been installed! Closing function")


def fetch_update():

    successfull = 100
    no_update = 0

    check_upgrade = ["dnf", "check-upgrade"]
    fetchUpdate = subprocess.run(check_upgrade, text=True, capture_output=True)

    logging.info("Checking for updates")
    if fetchUpdate.returncode is no_update:
        logging.info("No updates currently available. Exiting")
        sys.exit(0)

    elif fetchUpdate.returncode is not successfull:
        logging.info(f"Error occured! Exit code: {fetchUpdate.returncode}")
        sys.exit(1)

    else:
        logging.info("Updates available! Fetching..")
        logging.info("Updates successfully fetched!")
        logging.info("Attempting to create update manifest..")

        stdout = fetchUpdate.stdout.splitlines()
        try:
            with open(update_log, "w") as file:
                logging.info(f"Creating manifest located in {update_log}")

                for updates in stdout[2:]:
                    file.write(updates + "\n")

            logging.info("Finished! Closing function.")
            return True
        except OSError as err:
            logging.info(f"Error occured! {err}")
            sys.exit(1)


def send_email():

    logging.info("Preparing Email Message..")
    msg = EmailMessage()
    msg["Subject"] = "Update Manifest"
    msg["To"] = EMAIL
    msg["From"] = EMAIL
    msg.set_content("Update Manifest Attached")

    logging.info("Attaching update Manifest..")
    with open(update_log, "rb") as manifest:
        attach = manifest.read()
        file_name = manifest.name

    for part in msg.walk():
        maintype = part.get_content_maintype()
        subtype = part.get_content_subtype()

    logging.info("Message attached!")
    msg.add_attachment(attach, filename=file_name, maintype=maintype, subtype=subtype)

    logging.info("Logging into smtp.gmail.com..")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL, PASS)

            logging.info("Sending email")
            smtp.send_message(msg)
    except Exception as err:
        logging.info("An error occured while attempting to send the email message!")
        logging.info(err)
        sys.exit(1)


def main():

    if fetch_update():
        install_update()
        send_email()


if __name__ == "__main__":
    main()
