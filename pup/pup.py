#!/usr/bin/python3.7

# 1. sudo dnf check-upgrade > upgrade_list.txt to be emailed to me.
# 2. sudo dnf upgrade -y if successfull send an email to me if not send an email with the error.
# 3. close program.
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from config import credentials
from email import encoders

import subprocess
import pathlib
import logging
import smtplib
import socket
import ssl

# Logging Configurations
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')


# TODO: Finish install_update() function
# TODO: Refactor
# TODO: Add Time stamp info

def install_update():

    okay = 0
    command = ["dnf", "upgrade", "-y"]
    installUpdate = subprocess.run(command, text=True, capture_output=True)

    logging.info("Installing updates..")
    if installUpdate.returncode is not okay:
        logging.info("Error occured! Exiting Program..")
        error = f"Unable to install update. Error occured! {installUpdate.returncode}"
        logging.info(f"{error}")
        exit(1)
    else:
        logging.info("Updates has been installed! Exiting function..")


def fetch_update():

    okay = 100
    command = ["dnf", "check-upgrade"]
    fetchUpdate = subprocess.run(command, text=True, capture_output=True)

    logging.info("Fetching updates..")
    if fetchUpdate.returncode is not okay:
        logging.info("Error occured! Exiting Program..")
        error = f"Unable to fetch update. Error occured! {fetchUpdate.returncode}"
        logging.info(f"{error}")
        exit(1)

    else:
        logging.info("Updates fetched!")
        stdout = fetchUpdate.stdout.splitlines()
        logging.info("Attempting to open and create a text file..")
        try:
            logging.info("Text file created!")
            with open("textfile.txt", "w") as file:
                logging.info("Writing updates to text file..")
                for updates in stdout[2:]:
                    logging.info(updates)
                    file.write(updates + "\n")
            logging.info("Files has been written successfully! Closing function..")
            return True
        except OSError as err:
            logging.info("Error occured! File cannot be opened! Exiting Program..")
            exit(1)


def attachment():
    logging.info("Composing email message..")

    sender_email = credentials["email"]
    receiver_email = credentials["email"]

    outer = MIMEMultipart()
    outer["Subject"] = "Fedora Daily Updates"
    outer["To"] = receiver_email
    outer["From"] = sender_email

    attachments = pathlib.Path.cwd() / "textfile.txt"

    logging.info("Checking if attachment path exists..")
    if attachments.exists():
        logging.info("Attachment path exists! Attempting to create attachment payload..")
        try:
            with open(str(attachments), "rb") as fp:
                msg = MIMEBase("application", "octet-stream")
                msg.set_payload(fp.read())
                encoders.encode_base64(msg)
                msg.add_header('Content-Disposition', 'attachment', filename=attachments.name)
                outer.attach(msg)

                logging.info("Attachments successfully composed! Closing function..")
                composed = outer.as_string()
                return composed, sender_email, receiver_email
        except OSError as err:
            logging.info("Error occured when trying to compose attachment! Exiting Program..")
            logging.info(f"{err}")
            exit(1)
    else:
        logging.info(f"{attachments} does not exist! Exiting Program..")
        exit(1)


def send_email():
    logging.info("Gathering email account information..")
    port = 465
    smtp_server = "smtp.gmail.com"
    compose, sender, receiver = attachment()
    password = credentials["email_pw"]

    logging.info("Email account information gathered!")
    context = ssl.create_default_context()

    try:
        logging.info("Attempting to send email message..")
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, compose)
            logging.info("Email Successfully Sent!")
    except smtplib.SMTPConnectError as err:
        logging.info("Unable to connect to gmail server! Please check your network connection! Closing program..")
        exit(1)
    except smtplib.SMTPAuthenticationError as err:
        logging.info("Username and Password not accepted! Closing Program..")
        exit(1)
    except socket.error as err:
        logging.info("Error occured when trying to send email! Please check your network connection! Closing program")
        exit(1)


def main():

    logging.info("Running fetch_update() function")
    if fetch_update():
        logging.info("Running install_update() function")
        install_update()
        logging.info("Running attachment() function")
        attachment()
        logging.info("Running send_email() function")
        send_email()
        logging.info("End of script!")
        exit(0)
    else:
        logging.info("Unable to fetch update. Exiting Program..")
        exit(1)


if __name__ == "__main__":
    logging.info("Running main() method")
    main()
