from django.shortcuts import render

def contact_admin(request):
    return render(request, 'contact_admin/form.html', {})
