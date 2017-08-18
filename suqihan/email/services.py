from django.conf import settings
from django.core.mail import get_connection
from django.core.mail.message import EmailMultiAlternatives


def send_complex_mail(subject, message, from_email, to_email,cc,bcc,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None, html_message=None):
    """
    Easy wrapper for sending a single message to a recipient list. All members
    of the recipient list will see the other recipients in the 'To' field.

    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

    Note: The API for this method is frozen. New code wanting to extend the
    functionality should use the EmailMessage class directly.
    """
    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
    )
    mail = EmailMultiAlternatives(subject, message, from_email, to_email,cc=cc,bcc=bcc, connection=connection)
    if html_message:
        mail.attach_alternative(html_message, 'text/html')

    return mail.send()
    

def email(to_emails,cc=None,bcc=None,subject=None,content=None,html_message=None):
    if to_emails == None:
        return
    if subject == None:
        subject = ""
    if content == None:
        content = ""
    return send_complex_mail(
        subject,
        content,
        None,
        to_emails,
        cc,
        bcc,
        html_message = html_message,
        fail_silently=False,
    )
    
def template_email(to_emails,cc=None,bcc=None,template=None,resources=None):
    result = templateRender(template,resources);
    subject = result.get('title')
    content = result.get('content')
    is_html = template.is_html;
    if is_html:
        return email(to_emails,cc,bcc,subject,html_message=content);
    else:
        return email(to_emails,cc,bcc,subject,content);

def templateRender(template,resources):
    message = template.feed(resources);
    return message;

def test(to_emails):
    subject = "This is a test email to make sure your setting is correct"
    content = "your email setting for your project is correct"
    return email(to_emails,subject=subject,content=content)

if __name__ == "__main__":
    admins = [x[1] for x in settings.ADMINS]
    test(admins)
    