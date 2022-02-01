
from django.conf import settings
from django.core.checks import messages
from django.shortcuts import render
from .forms import NewsletterUserSignUpForm
from .models import NewsletterUser
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage

# Vista para que los usuarios se suscriban
def newsletter_signup(request):
    form = NewsletterUserSignUpForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email= instance.email).exists():
            messages.warning(request,'Email ya existe.')

        else: #si el usuario no existe, lo guardamos
            instance.save()
            messages.success(request,'Hemos enviado un correo electronico a su correo,abrelo para continuar con el entrenamiento')
            #Correo Electronico
            subject = "Libro de Robert Kiyosaki"
            from_email = settings.EMAIL_HOST_USER
            to_email=[instance.email] #Usuario que dejo el correo

            html_template='newsletters/email_templates/welcome.html'
            html_message= render_to_string(html_template)
            message = EmailMessage(subject,html_message,from_email,to_email)
            message.content_subtypes='html'
            message.send()


    return render(request,"start-here.html",{
        'form':form,
    })

def newsletter_unsubscribe(request):
    form = NewsletterUserSignUpForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            NewsletterUser.objects.filter(email=instance.email).delete()
            messages.succes(request,'Email ha sido removido')

        else:
            print('Email not found')
            messages.Warning(request,'Email no encontrado')

    return render(request,"unsubscribe.html",{
        "form": form,
    })
