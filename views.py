from django.shortcuts import get_object_or_404,render
from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import  timezone
from .models  import Question,Choice

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        return Question.objects.filter(pub_date=timezone.now()).order_by('pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


from django.template import loader
"""
def index(request):
    latest_question_list=Question.objects.order_by('-pub_date')[:5]
    template=loader.get_template('polls/index.html')
    context={
        'latest_question_list':latest_question_list,
    }
    output=','.join([q.question_text for q in latest_question_list])
    return HttpResponse(template.render(context,request))

def detail(request,question_id):
    return HttpResponse('You are looking at question %s'% question_id)
    try:
        question=Question.objects.get(pk=question_id)
        choice=Choice.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Question Does Not Exist!!!')
    return render(request,'polls/detail.html',{'question':question})

def results(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    return render(request,'polls/results.html',{'question':question})
    response='You are looking at the results of question %s'
    return HttpResponse(response%question_id)
"""
def vote(request,question_id):
    #return HttpResponse('You are voting on question %s'% question_id)
    question=get_object_or_404(Question,pk=question_id)
    #choice= get_object_or_404(Choice, pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except(KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{'question':question,'error_message':'Please select a choice!!!',})

    else:
        selected_choice.votes=F('votes')+2
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question_id,)))

# Create your views here.