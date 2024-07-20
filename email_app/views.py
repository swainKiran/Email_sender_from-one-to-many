from django.shortcuts import render

# Create your views here.

from django.core.mail import EmailMessage, get_connection
from django.http import HttpResponse

def index(request):
    return render(request, 'email_app/index.html')

def send_email(request):
    if request.method == 'POST':
        sender_email = request.POST['sender_email']
        email_password = request.POST['email_password']
        recipient_emails = request.POST['recipient_emails'].split(',')
        subject = request.POST['subject']
        message = request.POST['message']
        attachment = request.FILES.get('attachment')

        # Create a connection to the SMTP server using the provided credentials
        connection = get_connection(
            host='smtp.gmail.com',
            port=587,
            username=sender_email,
            password=email_password,
            use_tls=True
        )

        # Instantiate EmailMessage object
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=sender_email,
            to=recipient_emails,
            connection=connection,
        )

        # Attach the file if present
        if attachment:
            email.attach(attachment.name, attachment.read(), attachment.content_type)

        try:
            # Send email
            email.send(fail_silently=False)
            return render(request, 'email_app/success.html')
        except Exception as e:
            return HttpResponse(f"Failed to send emails: {e}")

    return HttpResponse("Invalid request method.")
