from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
import google.generativeai as genai
from google.generativeai.types.generation_types import StopCandidateException
from .models import ChatSession, ChatMessage
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@csrf_exempt
def chatbot(request):
    genai.configure(api_key='AIzaSyCKjBW9EB9XSQNwh__rARG6rc4nu8tTr6w')
    model = genai.GenerativeModel('gemini-pro')
    if request.user.is_authenticated:
        previous_chats = ChatSession.objects.filter(user=request.user)
    else:
        previous_chats = None
    if request.method == 'POST':
        
        # Start the chat with the history from the session
        chat = model.start_chat()

        user_in = request.POST.get('user_in', '')
        character_choice = request.POST.get('character_choice', '')
        media_choice = request.POST.get('media_choice', '')

        if user_in and character_choice and media_choice:
            response = None
            try:
                response = chat.send_message(f"respond to the following as if you were {character_choice} from {media_choice}: {user_in}")
            except StopCandidateException:
                response = type('', (), {})()
                response.text = "Sorry, I can't assist with that."
            print("Bot:", response.text)

            #if user is logged in, save the chat session and messages
            if request.user.is_authenticated:
                # Check if a ChatSession exists with the same character_choice and media_choice
                chat_session, created = ChatSession.objects.get_or_create(
                    character_choice=character_choice,
                    media_choice=media_choice,
                    user = request.user
                )

                # Create a new ChatMessage linked to the found or created ChatSession
                ChatMessage.objects.create(
                    chat_session=chat_session,
                    user_input=user_in,
                    generated_response=response.text
                )

            context = {
                'previous_chats': previous_chats,
                'character_choice': character_choice,
                'media_choice': media_choice,
                'user_in': user_in,
                'generated_text': response.text
            }
            return JsonResponse({
                'character_choice': character_choice,
                'media': media_choice,
                'user_in': user_in,
                'generated_text': response.text
                })
                
        else:
            return HttpResponse("Please provide user_in, character_choice, and media_choice as GET parameters.")
    else:
        context = {'previous_chats': previous_chats}
        return render(request, 'chatbot_app/generate_text.html', context)


@login_required
def clear_chats(request):
    if request.method == 'POST' and 'clear_chats' in request.POST:
        ChatSession.objects.all().delete()
    return HttpResponseRedirect(reverse('chatbot'))

@login_required
def clear_one_chat(request):
    if request.method == 'POST' and 'clear_one_chat' in request.POST:
        session_id = request.POST.get('session_id', '')
        if session_id:
            ChatSession.objects.filter(id=session_id).delete()
    return HttpResponseRedirect(reverse('chatbot'))

def get_chat_details(request, session_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        session = get_object_or_404(ChatSession, id=session_id)
        # Fetch user inputs and generated responses separately
        user_inputs = session.messages.all().order_by('created_at').values_list('user_input', flat=True)
        generated_responses = session.messages.all().order_by('created_at').values_list('generated_response', flat=True)
        
        # Interleave the two lists and flatten them
        messages = [item for pair in zip(user_inputs, generated_responses) for item in pair if item]
        
        response_data = {
        'character_choice': session.character_choice,
        'media_choice': session.media_choice,
        'messages': messages,
    }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

