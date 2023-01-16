from django.http import HttpResponse
from django.shortcuts import render, redirect
import os
from django.contrib.auth.decorators import login_required
import openai
from .models import ChatLog
from django.contrib.auth import authenticate, login, logout

openai.api_key = "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"


def chatbot_response(user_input):
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=user_input,
      temperature=0.7,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response["choices"][0]["text"]

@login_required(login_url="/login")
def chat_page(request):
    user = request.user
    if request.method == "POST":
        user_input = request.POST["msg"]
        response = chatbot_response(user_input)
        ChatLog.objects.create(user=user, send_msg=user_input, receive_msg=response)

    chat_data = ChatLog.objects.filter(user=user)[::-1]
    context = {'chat_data': chat_data}
    return render(request, "chat_bot.html", context=context)


def login_page(request):
    context = {'page': 'login_page'}
    if request.method == "POST":
        username = request.POST['email']
        user_password = request.POST['password']
        user = authenticate(username=username, password=user_password)
        if user:
            login(request, user)
            try:
                redirect_url = request.POST['redirect_url']
                return redirect(redirect_url)
            except:
                return render(request, "chat_bot.html", context=context)
        else:
            context['login_error'] = 'Email and Password Incorrect'
            return render(request, "login_page.html", context=context)

    else:
        try:
            context['redirect_url'] = request.GET['next']
        except:
            pass

        return render(request, "login_page.html", context=context)
