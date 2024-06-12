from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import google.generativeai as genai
from google.generativeai.types.generation_types import StopCandidateException

def chatbot(request):
    genai.configure(api_key='AIzaSyCKjBW9EB9XSQNwh__rARG6rc4nu8tTr6w')
    model = genai.GenerativeModel('gemini-pro')

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
            return JsonResponse({'character_choice':character_choice, 'media':media_choice, 'user_inp': user_in, 'generated_text': response.text})
                
        else:
            return HttpResponse("Please provide user_in, character_choice, and media_choice as GET parameters.")
    else:
        return render(request, 'generate_text.html')