from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView
from .services import *
import os

def home(request):
    if request.method == 'POST':
        text = request.POST['text']
        questions = generate_questions(text)
        
        # Debugging print
        print(f"Generated Questions: {questions}")
        
        context = {'questions': questions}
        return render(request, 'home.html', context)
    return render(request, 'home.html')

def history(request):
    return render(request, 'download.html')

def display_data():
    data = display()
    # Debugging print
    print(f"Display Data: {data}")
    return data

class TestListView(TemplateView):
    template_name = 'download.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = display_data()
        # Debugging print
        print(f"Context Data: {context['data']}")
        return context
    
def download(request, test_id):
    data = display_data()
    test = next((t for t in data if t[0] == test_id), None)

    if test:
        header = test[1]
        questions = test[2]
        filename = f'test_{test_id}.txt'

        with open(filename, 'w') as f:
            f.write(questions)

        file_path = os.path.join(os.getcwd(), filename)
        response = HttpResponse(open(file_path, 'rb'), content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={header}.txt'

        return response
    else:
        return HttpResponse('Test Not Found')
