 # nlpcalculator/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from nlpcalculator.Calculator import *
from nlpcalculator.forms import CalculatorForm

# Create your views here.


class HomeView(TemplateView):
  template_name = 'nlpcalculator/index.html'
		
  def get(self, request):
    form = CalculatorForm()
    return render(request, self.template_name, {'form': form})
	
  def post(self, request):
    form = CalculatorForm(request.POST)
    if form.is_valid():
      text = form.cleaned_data['inputQuery']

    args = {'form': form, 'result': showResult(text)}
    return render(request, self.template_name, args)    	  
	

			
 