from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse

from .models import Question, Choice


# These methods must all either return an HttpResponse or raise an exception


def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	# Using context dictionary (basically JSON) here allows us to pass variables in the template
	context = {
		'latest_question_list': latest_question_list,
	}
	# request object, template name, context dictionary (optional)
	return render(request, 'polls/index.html', context)


def detail(request, question_id):
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("Question does not exist")
	# A shortcut for try/catch 404 since it is so common
	# question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
	response = "You're looking at the results of question %s."
	return HttpResponse(response % question_id)


def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)

	try:
		# request.POST['choice'] refers to choice in the HTML
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# Redisplay the question voting form.
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))