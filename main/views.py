from django.shortcuts import render, redirect, get_object_or_404
from .models import AdminUser, Service, ServiceMedia
from .models import Service, ContactMessage
from .forms import ContactMessageForm



# Static Pages
def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def services(request):
    return render(request, 'main/services.html')



# Admin Logout
def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')

# Forgot Password
def forgot_password(request):
    message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            admin = AdminUser.objects.get(username=username)
            message = f"Hi {admin.username}, please contact superadmin to reset your password."
        except AdminUser.DoesNotExist:
            message = "Username not found."
    return render(request, 'main/forgot_password.html', {'message': message})

# Admin Login
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            admin = AdminUser.objects.get(username=username, password=password)
            request.session['admin_logged_in'] = True
            return redirect('admin_dashboard')
        except AdminUser.DoesNotExist:
            return render(request, 'admin_login.html', {'error': 'Invalid credentials'})
    return render(request, 'admin_login.html')

# Admin Dashboard with services and contact
from .models import Service, ContactMessage, StudioContact
from .forms import StudioContactForm
from django.contrib import messages
from django.shortcuts import render, redirect

def admin_dashboard(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    services = Service.objects.all()
    inquiries = ContactMessage.objects.all().order_by('-created_at')

    # Get or create the contact info (assuming only one record)
    contact_info, created = StudioContact.objects.get_or_create(pk=1)

    # Handle contact info update
    if request.method == 'POST' and 'update_contact' in request.POST:
        contact_form = StudioContactForm(request.POST, instance=contact_info)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, "Studio contact information updated successfully.")
            return redirect('admin_dashboard')
    else:
        contact_form = StudioContactForm(instance=contact_info)

    return render(request, 'admin_dashboard.html', {
        'services': services,
        'inquiries': inquiries,
        'contact_form': contact_form,
    })




from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, ServiceMedia

def upload_media(request):
    if not request.session.get('admin_logged_in'):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)
        return redirect('admin_login')

    if request.method == 'POST':
        service_id = request.POST.get("service_id")
        caption = request.POST.get("caption", "")
        service = get_object_or_404(Service, id=service_id)

        # Save caption on Service
        if caption:
            service.caption = caption
            service.save()

        # Save uploaded files
        for file in request.FILES.getlist("media_file"):
            ServiceMedia.objects.create(
                service=service,
                media_file=file,
                caption=caption
            )

        # ✅ If AJAX request, return JSON response
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Media uploaded successfully.'})

        # ✅ For normal form POST
        messages.success(request, "Media uploaded successfully.")
        return redirect('/admin-dashboard/?section=media')

    return redirect('/admin-dashboard/?section=media')

# Update Studio Contact Info


# Service Detail Page (for frontend)
def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    media = service.media.all()  # uses related_name='media'
    return render(request, 'main/service_detail.html', {
        'service': service,
        'media': media
    })


# Rename a Service
from django.contrib import messages

def rename_service(request, service_id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    
    service = get_object_or_404(Service, id=service_id)
    
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        if new_name:
            service.name = new_name
            service.save()
            messages.success(request, 'Name changed successfully.')
        else:
            messages.error(request, 'Name cannot be empty.')
    
    return redirect('admin_dashboard')




from django.shortcuts import redirect, get_object_or_404
from .models import ServiceMedia

def delete_media(request, media_id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    media = get_object_or_404(ServiceMedia, id=media_id)
    media.delete()

    section = request.GET.get('section', 'category')
    return redirect(f'/admin-dashboard/?section={section}')


from .models import Service

def services_page(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})


from django.http import JsonResponse
from .models import ServiceMedia

def delete_media_ajax(request, media_id):
    if not request.session.get('admin_logged_in'):
        return JsonResponse({'success': False, 'error': 'Not authorized'}, status=403)

    if request.method == "POST":
        try:
            media = ServiceMedia.objects.get(id=media_id)
            media.delete()
            return JsonResponse({'success': True})
        except ServiceMedia.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Media not found'}, status=404)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

from .models import StudioContact  # Make sure you import this at the top

from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
def contact(request):
    contact_info = StudioContact.objects.first()

    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            contact_message = form.save()

            # Prepare HTML email
            subject = "📩 New Inquiry from Studio 85 Website"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = ['ststudio85@gmail.com']

            html_content = f"""
            <div style="font-family: Arial, sans-serif; border: 1px solid #ddd; padding: 20px; border-radius: 10px; background-color: #fefefe;">
              <h2 style="color: #795757;">📸 Studio 85 - New Inquiry Received</h2>
              <hr style="margin: 10px 0;">
              <p><strong>Name:</strong> {contact_message.name}</p>
              <p><strong>Email:</strong> {contact_message.email}</p>
              <p><strong>Mobile:</strong> {contact_message.mobile}</p>
              <p><strong>Message:</strong><br>{contact_message.inquiry}</p>
              <hr style="margin: 20px 0;">
              <p style="font-size: 12px; color: #777;">Submitted on: {contact_message.created_at.strftime('%d %B %Y, %I:%M %p')}</p>
            </div>
            """

            text_content = strip_tags(html_content)  # Fallback for email clients that don't support HTML

            email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            email.attach_alternative(html_content, "text/html")
            email.send()

            return render(request, 'main/contact.html', {
                'form': ContactMessageForm(),
                'success': True,
                'contact_info': contact_info
            })

    else:
        form = ContactMessageForm()

    return render(request, 'main/contact.html', {
        'form': form,
        'contact_info': contact_info
    })



from django.shortcuts import get_object_or_404, redirect
from .models import ContactMessage

def delete_inquiry(request, msg_id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    inquiry = get_object_or_404(ContactMessage, id=msg_id)

    if request.method == 'POST':
        inquiry.delete()

    return redirect('/admin-dashboard/?section=inquiries')



