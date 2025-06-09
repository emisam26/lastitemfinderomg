from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.
def contact(request):
    if request.method == 'POST':
        item_id = request.POST['item_id']
        item = request.POST['item']
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        user_id = request.POST['user_id']
        
        # if user has already made na inquiry
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(item_id=item_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You already made an inquiry for the item!')
                return redirect('/found_items/' + item_id) 
        contact = Contact(item=item, item_id=item_id, name=name, email=email, message=message, user_id=user_id)
        contact.save()
        
        # send an email to the admin
        send_mail(
            "Property",
            "There has been an inquiry for " + item + ". Sign into the admin panel for more information." ,
            "lily18570@gmail.com", # your email
            ["emisam26@bergen.org"], # admin/recipient email
            fail_silently=False,
        )
        
        messages.success(request, "Your request submitted! An admin will get back to you soon!")
        return redirect('/found_items/'+item_id)