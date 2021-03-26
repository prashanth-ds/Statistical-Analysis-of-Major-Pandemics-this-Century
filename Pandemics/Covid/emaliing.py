from django.core.mail.message import EmailMessage


def email(name, subject, mailid, file_path):
    email = EmailMessage("Respected, {}!!".format(name),
                         subject,
                         to=[mailid])

    email.attach_file(file_path)
    email.send()
    print("Email Sent")

