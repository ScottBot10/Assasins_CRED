import imaplib
import logging
import smtplib
import sys
import typing as t
from email.message import EmailMessage

from easyimap.easyimap import MailObj
# noinspection PyProtectedMember
from easyimap.easyimap import _parse_email as parse_email

import config
from .constants import EMAIL_FROM_FORMAT
from .school import Student

logger = logging.getLogger("assassins_cred")


def clear_inbox(email, password, mail_box="Inbox") -> None:
    with imaplib.IMAP4_SSL("imap.gmail.com") as m:
        m.login(email, password)
        m.select(mail_box)
        resp, data = m.uid('search', None, "ALL")
        uids = data[0].split()
        for uid in uids:
            m.uid('fetch', uid, "(BODY[HEADER])")
            m.uid('STORE', uid, '+FLAGS', '(\\Deleted)')
        m.select('"[Gmail]/Trash"')
        m.store("1:*", '+FLAGS', '\\Deleted')
        m.expunge()
        logger.info(f"Deleted all emails from {mail_box}")


def send_email(
        to_address: str,
        from_address: str,
        title: str,
        body: str,
        smtp: smtplib.SMTP = None,
        password: str = None) -> None:
    if smtp is None:
        if password is None:
            raise ValueError("Specify either smtp or password")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            try:
                smtp.login(from_address, password)
            except smtplib.SMTPAuthenticationError:
                logger.error('Turn on less secure access or check if you have the correct password')
                return
            send_email(to_address, from_address, title, body, smtp)
    else:
        msg = EmailMessage()

        msg["Subject"] = title
        msg["From"] = from_address
        msg["To"] = to_address
        msg.set_content(body)

        smtp.send_message(msg)
        logger.debug(f'Email "{msg["Subject"]}" sent from "{msg["From"]}" to "{msg["To"]}"')


def send_to_each(students: t.Sequence[Student],
                 title: str,
                 body: str,
                 from_address: str,
                 smtp: smtplib.SMTP = None,
                 to_address=None,
                 password: str = None,
                 format_kws=None) -> None:
    for student in students:
        send_email(
            to_address=to_address or f"{student.email}@{config.email.domain}",
            from_address=from_address,
            title=title,
            body=body.format(
                student=student,
                **format_kws),
            smtp=smtp,
            password=password
        )


def process_incoming_mail(smtp: smtplib.SMTP,
                          mail: MailObj,
                          students: t.Dict[str, Student],
                          from_address: str,
                          config) -> bool:
    if mail.title.lower() == config.email.subject:
        match = EMAIL_FROM_FORMAT.match(mail.from_addr)
        if match is not None:
            address = match.groupdict()["address"]
            if address in students:
                student = students[address]
                if not student.has_killed:
                    if not student.is_dead:
                        if student.target.code in mail.body.lower().strip():
                            send_email(
                                to_address=student.full_email,
                                from_address=from_address,
                                title=config.email.titles.success,
                                body=config.email.contents.success.format(student=student),
                                smtp=smtp
                            )
                            send_email(
                                to_address=config.creds.test_to if config.is_test else student.target.full_email,
                                from_address=from_address,
                                title=config.email.titles.assassinated,
                                body=config.email.contents.assassinated.format(student=student),
                                smtp=smtp
                            )
                            student.has_killed = True
                            student.target.is_dead = True
                            logger.info(f"{student} has killed {student.target}")
                            return True
                        else:
                            send_email(
                                to_address=student.full_email,
                                from_address=from_address,
                                title=config.email.titles.failure,
                                body=config.email.contents.failure.format(student=student),
                                smtp=smtp
                            )
                            logger.info(f"{student} tried to kill {student.target} but sent the wrong code")
                    else:
                        send_email(
                            to_address=student.full_email,
                            from_address=config.creds.email,
                            title=config.email.titles.dead,
                            body=config.email.contents.dead.format(student=student),
                            smtp=smtp
                        )
                        logger.info(f"{student} tried to kill {student.target} but is already dead")
    return False


def get_mail(smtp: smtplib.SMTP, imap: imaplib.IMAP4, students: t.Dict[str, Student], config: Config) -> bool:
    imap.select()
    bs = []
    (retcode, messages) = imap.search(None, '(UNSEEN)')
    if retcode == 'OK':
        if messages == [b'']:
            imap.expunge()
            return
        logger.debug(f"New messages found")
        try:
            for num in messages[0].split(b' '):
                typ, data = imap.fetch(num, '(RFC822)')
                mail = parse_email(data)
                imap.store(num, '+FLAGS', '\\Seen')
                b = process_incoming_mail(
                    smtp=smtp,
                    mail=mail,
                    students=students,
                    from_address=config.creds.email,
                    config=config
                )
                bs.append(b)
        except:
            logger.error(sys.exc_info()[1])
    return any(bs)
