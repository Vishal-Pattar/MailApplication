import flet as ft
from smtplib import SMTP_SSL
from SMPT import SMPTProvider
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Function to validate email input fields
def validate(from_mailid, mailpassword, to_mailid, mailsubject, mailbody):
    res = True
    if len(from_mailid.value) == 0:
        from_mailid.error_text = "Can't be empty!"
        res = False
    if len(mailpassword.value) == 0:
        mailpassword.error_text = "Can't be empty!"
        res = False
    if len(to_mailid.value) == 0:
        to_mailid.error_text = "Can't be empty!"
        res = False
    if len(mailsubject.value) == 0:
        mailsubject.error_text = "Can't be empty!"
        res = False
    if len(mailbody.value) == 0:
        mailbody.error_text = "Can't be empty!"
        res = False
    return res

# Function to send email
def send_mail(from_mailid, mailpassword, to_mailid, mailsubject, mailbody, mailattach):
    # Get SMTP server details
    service = SMPTProvider(from_mailid)
    host = service.server()
    port = service.portSSL()

    # Establish SSL connection
    try:
        smtp_ssl = SMTP_SSL(host=host, port=port)
    except Exception as e:
        smtp_ssl = None

    # Login to SMTP server
    resp_code, response = smtp_ssl.login(user=from_mailid, password=mailpassword)
    print("1", resp_code, response)

    # Create email message
    message = MIMEMultipart('alternative')
    message["From"] = from_mailid
    message["To"] = to_mailid
    message["Subject"] = mailsubject
    message.attach(MIMEText(mailbody))

    # Attach files if present
    if mailattach.find('.') != -1:
        attarr = [mailattach] if mailattach.count('.') == 1 else mailattach.split(",")
        for xatt in attarr:
            fext = xatt.split('.')[-1]
            flname = xatt.split('\\')[-1]
            with open(xatt, 'rb') as f:
                mime = MIMEBase('document', fext, filename=xatt)
                mime.add_header('Content-Disposition', 'attachment', filename=flname)
                mime.add_header('X-Attachment-Id', '0')
                mime.add_header('Content-ID', '<0>')
                mime.set_payload(f.read())
                encoders.encode_base64(mime)
                message.attach(mime)

    # Send email
    response = smtp_ssl.send_message(msg=message)
    print("2", response)
    resp_code, response = smtp_ssl.quit()
    print("3", resp_code, response)

# Main function to setup Flet UI
def main(page: ft.Page):
    page.title = "Mail App"
    page.window_height = 800
    page.window_width = 600
    page.window_resizable = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # UI elements
    head = ft.Text("Mail App", size=25, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.W_900)
    from_email = ft.TextField(label="From", hint_text="Enter your email address", content_padding=10)
    password = ft.TextField(label="Password", hint_text="Enter your Password", password=True, can_reveal_password=True, content_padding=10)
    to_email = ft.TextField(label="To", hint_text="Enter recipient's email address", content_padding=10)
    subject = ft.TextField(label="Subject", content_padding=10, multiline=True, max_lines=3)
    body = ft.TextField(label="Body", content_padding=10, min_lines=10, multiline=True)

    # Button click event handler
    def btn_click(e):
        if validate(from_email, password, to_email, subject, body):
            send_mail(from_email.value, password.value, to_email.value, subject.value, body.value, attach_path.value)
        # Clear input fields
        to_email.value = ""
        subject.value = ""
        body.value = ""
        attach_files.value = ""
        attach_path.value = ""
        page.update()

    # File picker result event handler
    def pick_files_result(e: ft.FilePickerResultEvent):
        attach_files.value = ", ".join([f.name for f in e.files]) if e.files else "Cancelled!"
        attach_path.value = ",".join([f.path for f in e.files]) if e.files else "Cancelled!"
        page.update()

    # File picker dialog
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)
    attach_files = ft.Text("")
    attach_path = ft.Text("")

    # Layout setup
    col = ft.Column([
        ft.Container(content=head, alignment=ft.alignment.bottom_center),
        ft.Container(content=from_email),
        ft.Container(content=password),
        ft.Container(content=to_email),
        ft.Container(content=subject),
        ft.Container(content=body),
        ft.Container(
            ft.Row([
                ft.ElevatedButton(
                    "Add Attachment",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True),
                ),
                attach_files,
            ])
        ),
        ft.Container(
            content=ft.ElevatedButton("Send Message", on_click=btn_click, color="#000000"),
            padding=5,
            alignment=ft.alignment.bottom_center,
        )
    ], width=400)

    cont = ft.Container(
        content=col,
        padding=20,
        border_radius=10,
        border=ft.border.all(2, '#000000'),
    )

    page.add(cont)

ft.app(target=main)
