from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, Http404
from .models import Question

from django.template import loader
# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    # context = {
    #     'latest_question_list': latest_question_list,
    # }
    # return HttpResponse(template.render(context, request))
    # 以下语句功能同上
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, 'polls/detail.html', {'question': question})
    # 以下语句功能同上
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request,question_id):
    return HttpResponse("你看到的是问题[ %s ]的结果"%question_id)

def vote(request,question_id):
    return HttpResponse("你看到的是问题[ %s ]的投票"%question_id)