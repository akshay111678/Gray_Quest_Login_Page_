from django.http import HttpResponse
from django.shortcuts import render

def home_page(request):
  content="The right way to pay for Education in India."
  data = {'content':content}
  if request.user.is_authenticated:
    data['msg'] = request.user
  return render(request,"home.html",data)


