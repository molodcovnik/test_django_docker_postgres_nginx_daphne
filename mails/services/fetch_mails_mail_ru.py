import datetime
import imaplib
import email
from email.header import decode_header
import quopri
import base64
from email.utils import parsedate_tz, mktime_tz

from langdetect import detect
import binascii

from mails.services.counter import update_account_count
from mails.services.messages import create_new_email_message


def decode_header_value(header_value):
    """Декодировать заголовок, если он закодирован"""

    if header_value is None:
        return ""
    decoded_parts = decode_header(header_value)
    decoded_header = ''
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            decoded_header += part.decode(encoding or 'utf-8', errors='replace')
        else:
            decoded_header += part
    return decoded_header


def decode_text(text, encoding):
    """Декодировать текст с учетом кодировки"""
    if text is None:
        return ''
    if isinstance(text, bytes):
        try:
            return text.decode(encoding or 'utf-8')
        except (UnicodeDecodeError, TypeError):
            return text.decode('latin-1')  # Попытка другой кодировки при неудаче
    return text


def fix_base64_padding(text):
    """Исправить дополнение base64"""
    if isinstance(text, bytes):
        text = text.decode('utf-8')
    missing_padding = len(text) % 4
    if missing_padding:
        text += '=' * (4 - missing_padding)
    return text


def get_email_body(msg):
    """Получить тело письма"""

    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if "attachment" not in content_disposition:
                body = part.get_payload(decode=True)
                if body:
                    content_transfer_encoding = part.get('Content-Transfer-Encoding')
                    try:
                        if content_transfer_encoding == 'quoted-printable':
                            body = quopri.decodestring(body)
                        elif content_transfer_encoding == 'base64':
                            body = base64.b64decode(fix_base64_padding(body))
                    except (binascii.Error, ValueError) as e:
                        print(f"Decoding error: {e}")
                    return decode_text(body, part.get_content_charset())
    else:
        body = msg.get_payload(decode=True)
        content_transfer_encoding = msg.get('Content-Transfer-Encoding')

        try:
            if content_transfer_encoding == 'quoted-printable':
                body = quopri.decodestring(body)
            elif content_transfer_encoding == 'base64':
                body = base64.b64decode(fix_base64_padding(body))
        except (binascii.Error, ValueError) as e:
            print(f"Decoding error: {e}")
        return decode_text(body, msg.get_content_charset())
    return body


def get_text_snippet(text, length=100):
    """Получить небольшой фрагмент текста"""
    return text[:length] if text else ''


def detect_language(text):
    """Определить язык текста"""
    try:
        lang = detect(text)
        return 'Russian' if lang == 'ru' else 'English' if lang == 'en' else 'Unknown'
    except:
        return 'Unknown'


def get_attachments(msg):
    """Получить список вложений"""
    attachments = []
    if msg.is_multipart():
        for part in msg.walk():
            content_disposition = str(part.get("Content-Disposition"))
            if "attachment" in content_disposition:
                filename = part.get_filename()
                if filename:
                    decoded_filename = decode_header_value(filename)
                    attachments.append(decoded_filename)
    return attachments


def get_messages_mail(account_id: int, username: str, password: str):
    mail = imaplib.IMAP4_SSL("imap.mail.ru")
    try:
        mail.login(username, password)
    except imaplib.IMAP4.error as e:
        print(f"Ошибка входа: {e}")
        return
    except Exception as e:
        print(f"Произошла неожиданная ошибка: {e}")
        return

    # Выбор почтового ящика (inbox)
    mail.select("inbox")

    # Поиск всех писем в папке "inbox"
    status, messages = mail.search(None, 'ALL')
    messages = messages[0].split()
    for i in range(len(messages)):
        update_account_count(account_id, i + 1)
    for mail_id in messages:
        # Получение данных письма (raw)
        status, data = mail.fetch(mail_id, "(RFC822)")
        raw_email = data[0][1]

        msg = email.message_from_bytes(raw_email)

        subject = decode_header_value(msg.get("Subject"))
        from_ = decode_header_value(msg.get("From"))
        date = msg.get("Date")
        body = get_email_body(msg)

        if date:
            date_tuple = parsedate_tz(date)
            if date_tuple:
                sent_date = datetime.datetime.fromtimestamp(mktime_tz(date_tuple))
            else:
                sent_date = None
        else:
            sent_date = None

        body_snippet = get_text_snippet(body, length=100)

        language = detect_language(body)

        attachments = get_attachments(msg)

        create_new_email_message(account_id, uid=int(mail_id), subject=subject, sent_date=sent_date,
                                 received_date=sent_date, message_text=body_snippet, attachments=attachments)

    mail.logout()
