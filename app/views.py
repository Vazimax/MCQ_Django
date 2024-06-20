from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView
from .services import *
import os

def home(request):

    if request.method == 'POST':
        text = request.POST['text']
        questions = generate_questions(text)
        
        context = {'questions':questions}
        return render(request, 'home.html', context)


    return render(request, 'home.html')

def history(request):

    return render(request,'download.html')

data = display()

class TestListView(TemplateView):
    template = 'download.html'
    def get_context(self, **kwargs):
        context = super().get_context(**kwargs)
        context['data'] = data

        return context
    
def download(request,test_id):
    test = next((t for t in data if t[0] == test_id), None)

    if test:
        header = test[1]
        questions = test[2]
        filename = f'test_{test_id}.txt'

        with open(filename, 'w') as f:
            f.write(questions)

        file_path = os.path.join(os.getcwd(), filename)
        response = HttpResponse(open(file_path,'rb'),content_type='text/plain')
        response['Content-Description'] = f'attachment; filename= {header}.txt'

        return response
    
    else:
        return HttpResponse('Test Is Not Found')
