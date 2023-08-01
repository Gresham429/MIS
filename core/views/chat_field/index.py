from django.shortcuts import render


def chat_field_index(request):
    context = {
        'current_user': request.user.username
    }
   
    return render(request, 'chat_field/chat_field.html', context)