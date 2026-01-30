from django.shortcuts import render

# Dashboard home page - Welcome screen
def dashboard_home(request):
    context = {
        'page_title': 'Dashboard',
    }
    return render(request, 'dashboard/home.html', context)
