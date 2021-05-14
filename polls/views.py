from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
# from django.template import loader
from django.urls import reverse
from django.views import generic
from .models import Question,Choice

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context = 'latest_question_list'

    def get_queryset(self):
        latest_question_list = Question.objects.order_by('-pub_date')[:5]



    # template_name = 'polls/index.html'
    # context = {
    #     'latest_question_list': latest_question_list,
    # }
    # return render(request,'polls/index.html',context)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


    
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise get_object_or_404(Question,pk=question_id)
    # return render(request,'polls/detail.html',{'question':question})        
    # return HttpResponse("You're looking at question %s."% question_id)

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'



def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

    except(KeyError, Choice.DoesNotExist):
        #Redisplays the question voting form
        return render(request,'polls/detail.html',{
            'question':question,
            'error_message':"You didn't seclect a choice .",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results',args=(question.id)))
