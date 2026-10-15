from django.shortcuts import render

def main_func(request):
    return render(request, template_name='main.html')
