from django.shortcuts import render

# Create your views here.

def homeView(request):
    template = 'mainapp/home.html'
    context = {}

    return render(request, template_name= template, context= context)



def aboutView(request):
    template = 'mainapp/about.html'
    context = {}

    return render(request, template_name= template, context= context)


def contactView(request):
    template = 'mainapp/contact.html'
    context = {}

    return render(request, template_name= template, context= context)



    

    