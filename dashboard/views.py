
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView,View,UpdateView,DeleteView
from newsletters.models import Newsletter
from newsletters.forms import NewsletterCreationForm

from django.core.mail import send_mail,EmailMultiAlternatives, EmailMessage

class DashboardHomeView(TemplateView):
    template_name= "dashboard/index.html"

class NewslettersDashboardHomeView(View):
    def get(self,request,*args,**kwargs):
        newsletters= Newsletter.objects.all()
        return render(request,'dashboard/list.html',{'newsletters':newsletters})

#CREAR 
class NewslettersCreateView(View):
    def get(self,request, *args, **kwargs):
        form = NewsletterCreationForm()
        return render(request,'dashboard/create.html',{'form':form})

    def post(self,request, *args, **kwargs):
        if request.method=="POST":
            form = NewsletterCreationForm(request.POST or None)
            if form.is_valid():
                instance=form.save()
                newsletter=Newsletter.objects.get(id=instance.id)
                
                if newsletter.status=="Published":
                    subject = newsletter.subject
                    body = newsletter.body
                    from_email = settings.EMAIL_HOST_USER
                    for email in newsletter.email.all():
                        send_mail(subject=subject,from_email=from_email, recipient_list=[email], message=body,fail_silently=True)

                return redirect ('dashboard:list')


        return render(request,'dashboard/create.html',{'form':form})

class NewsletterDetailView(View):
    def get(self, request, pk,*args, **kwargs):
        newsletter=get_object_or_404(Newsletter,pk=pk)
        return render(request, 'dashboard/detail.html', {'newsletter':newsletter})



#ACTUALIZAR
class NewsletterUpdateView(UpdateView):
    model=Newsletter
    form_class=NewsletterCreationForm
    template_name='dashboard/update.html'
    success_url='/dashboard/detail/2/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type':'update'
        })
        return context

    def post(self, request, pk, *args, **kwargs):
        newsletter=get_object_or_404(Newsletter, pk=pk)

        if request.method=="POST":
            form=NewsletterCreationForm(request.POST or None)

            if form.is_valid():
                instance=form.save()
                newsletter=Newsletter.objects.get(id=instance.id)

                if newsletter.status=="Published":
                    subject = newsletter.subject
                    body = newsletter.body
                    from_email = settings.EMAIL_HOST_USER
                    for email in newsletter.email.all():
                        send_mail(subject=subject, from_email=from_email, recipient_list=[email], message=body, fail_silently=True)
                return redirect('dashboard:detail', pk=newsletter.id)
            return redirect('dashboard:detail', pk=newsletter.id)
        else:
            form=NewsletterCreationForm(instance=newsletter)

        return render(request, 'dashboard/update.html', {'form':form})



#ELIMINAR
class NewsletterDeleteView(DeleteView):
    model=Newsletter
    template_name='dashboard/delete.html'
    success_url='/dashboard/list/'