from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserResponseForm
from .models import Question, Answer, UserAnswer


def single(request, pk):
    if request.user.is_authenticated():
        # queryset = Question.objects.all().order_by('-timestamp')
        instance = get_object_or_404(Question, pk=pk)

        try:
            user_answer = UserAnswer.objects.get(
                user=request.user, question=instance)
        except UserAnswer.DoesNotExist:
            user_answer = UserAnswer()
        except UserAnswer.MultipleObjectsReturned:
            user_answer = UserAnswer.objects.filter(
                user=request.user, question=instance)[0]
        except:
            user_answer = UserAnswer()

        form = UserResponseForm(request.POST or None)
        if form.is_valid():

            question_id = form.cleaned_data['question_id']
            answer_id = form.cleaned_data['answer_id']
            important_level = form.cleaned_data['important_level']

            their_important_level = form.cleaned_data['their_important_level']
            their_answer_id = form.cleaned_data['their_answer_id']

            question_instance = Question.objects.get(pk=question_id)
            answer_instance = Answer.objects.get(pk=answer_id)

            user_answer.user = request.user
            user_answer.question = question_instance
            user_answer.my_answer = answer_instance
            user_answer.my_answer_importance = important_level
            if their_answer_id != -1:
                their_answer_instance = Answer.objects.get(
                    pk=their_answer_id)
                user_answer.their_answer = their_answer_instance
                user_answer.their_importance = their_important_level
            else:
                user_answer.their_answer = None
                user_answer.their_importance = "Not Important"
            user_answer.save()

            next_q = Question.objects.all().order_by('?').first()
            return redirect("question_single", pk=next_q.pk)

        context = {
            "form": form,
            "instance": instance,
            "user_answer": user_answer,
            # "queryset": queryset
        }
        return render(request, "questions/single.html", context)
    else:
        raise Http404


def home(request):
    if request.user.is_authenticated():
        form = UserResponseForm(request.POST or None)
        if form.is_valid():
            question_id = form.cleaned_data['question_id']
            answer_id = form.cleaned_data['answer_id']
            question_instance = Question.objects.get(pk=question_id)
            answer_instance = Answer.objects.get(pk=answer_id)
            print question_instance.text, answer_instance.text

        queryset = Question.objects.all().order_by('-timestamp')
        instance = queryset[1]
        context = {
            "form": form,
            "instance": instance,
            # "queryset": queryset
        }
        return render(request, "questions/home.html", context)
    else:
        raise Http404
