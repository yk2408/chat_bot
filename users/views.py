from django.http import HttpResponse
from django.shortcuts import render
import os
import openai
from .models import ChatLog

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


def chat_page(request):
    user = request.user
    if request.method == "POST":
        user_input = request.POST["msg"]
        response = chatbot_response(user_input)
        ChatLog.objects.create(user=user, send_msg=user_input, receive_msg=response)

    chat_data = ChatLog.objects.filter(user=user)[::-1]
    context = {'chat_data': chat_data}
    return render(request, "chat_bot.html", context=context)
