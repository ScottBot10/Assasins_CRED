# noinspection PyProtectedMember
import imaplib
import re
import smtplib
import sys
import typing as t
from email.message import EmailMessage

from easyimap.easyimap import MailObj
from easyimap.easyimap import _parse_email as parse_email

from assassins_cred.constants import Email
from assassins_cred.school import Student
from assassins_cred.util.config import Config

EMAIL_ADDRESS = re.compile(r"(?P<from>.+) <(?P<email>(?P<address>[a-zA-Z.]+)@(?P<domain>[a-zA-Z.]+))>")


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
                print('Turn on less secure access or check if you have the correct password')
                return
            send_email(to_address, from_address, title, body, smtp)
    else:
        msg = EmailMessage()

        msg["Subject"] = title
        msg["From"] = from_address
        msg["To"] = to_address
        msg.set_content(body)

        smtp.send_message(msg)


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
            to_address=to_address or f"{student.email}@{Email.email_domain}",
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
                          config: Config) -> None:
    if mail.title.lower() == Email.email_subject:
        match = EMAIL_ADDRESS.match(mail.from_addr)
        if match is not None:
            address = match.groupdict()["address"]
            if address in students:
                student = students[address]
                if not student.has_killed:
                    if not student.is_dead:
                        print(student.target.code)
                        print(mail.body.lower().strip())
                        if student.target.code in mail.body.lower().strip():
                            send_email(
                                to_address=student.full_email,
                                from_address=from_address,
                                title=Email.Titles.email_success,
                                body=Email.email_success.format(student=student),
                                smtp=smtp
                            )
                            send_email(
                                to_address=config.creds["test_to"] if config.is_test else student.target.full_email,
                                from_address=from_address,
                                title=Email.Titles.email_assassinated,
                                body=Email.email_assassinated.format(student=student),
                                smtp=smtp
                            )
                            student.has_killed = True
                            student.target.is_dead = True
                        else:
                            send_email(
                                to_address=student.full_email,
                                from_address=from_address,
                                title=Email.Titles.email_failure,
                                body=Email.email_failure.format(student=student),
                                smtp=smtp
                            )
                    else:
                        send_email(
                            to_address=student.full_email,
                            from_address=config.creds["email"],
                            title=Email.Titles.email_dead,
                            body=Email.email_dead.format(student=student),
                            smtp=smtp
                        )


def get_mail(smtp: smtplib.SMTP, imap: imaplib.IMAP4, students: t.Dict[str, Student], config: Config):
    imap.select()
    (retcode, messages) = imap.search(None, '(UNSEEN)')
    if retcode == 'OK':
        if messages == [b'']:
            imap.expunge()
            return
        try:
            for num in messages[0].split(b' '):
                typ, data = imap.fetch(num, '(RFC822)')
                mail = parse_email(data)
                imap.store(num, '+FLAGS', '\\Seen')
                process_incoming_mail(
                    smtp=smtp,
                    mail=mail,
                    students=students,
                    from_address=config.creds["email"],
                    config=config
                )
        except:
            print(sys.exc_info()[1])
