from django.shortcuts import render


def dashboard_home(request):
    """
    Dashboard home page - Welcome screen
    """
    context = {
        'page_title': 'Dashboard',
    }
    return render(request, 'dashboard/home.html', context)
