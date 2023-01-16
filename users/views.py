from django.http import HttpResponse
from django.shortcuts import render, redirect
import os
from django.contrib.auth.decorators import login_required
import openai
from .models import ChatLog
from .models import User
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
    context = {'chat_data': chat_data, 'name': user.full_name}
    return render(request, "chat_bot.html", context=context)


def login_page(request):
    context = {'page': 'login_page'}
    if request.method == "POST":
        email = request.POST['email']
        user_password = request.POST['password']
        user = authenticate(email=email, password=user_password)
        if user:
            login(request, user)
            try:
                redirect_url = request.POST['redirect_url']
                return redirect(redirect_url)
            except:
                return redirect("/chat-page")
        else:
            context['login_error'] = 'Email and Password Incorrect'
            return render(request, "login_page.html", context=context)

    else:
        try:
            context['redirect_url'] = request.GET['next']
        except:
            pass

        return render(request, "login_page.html", context=context)


def register_page(request):
    if request.method == "POST":
        email = request.POST['email']
        user_password = request.POST['password']
        name = request.POST['name']
        mobile_number = request.POST['mobile_number']
        user = User(email=email, full_name=name, phone_number=mobile_number)
        user.set_password(user_password)
        user.save()
        return redirect("/chat-page")

    return render(request, "sign_up.html")

