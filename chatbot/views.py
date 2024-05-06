# shopbot/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .shopbot import get_completion_from_messages
from django.shortcuts import render

product_list = '''
  # Social Media Marketing

  ## YouTube Services:

  - YouTube Views  
    - Price per 1000 Views: $9.99
    - Guide prompt: please put your youtube VIDEO Link  
    
  - YouTube Subscribers  
    - Price per 1000 Subscribers: $14.99
    - Guide prompt: please put your youtube CHANNEL Link  

  - YouTube Likes
    - Price per 1000 Likes: $4.49
    - Guide prompt: please put your youtube VIDEO Link  

  - YouTube Comments
    - Price per 1000 Comments: $6.49
    - Guide prompt: please put your youtube VIDEO Link  


  ## Facebook Services:
  - Facebook Followers  
    - Price per 1000 Followers: $11.99
    - Guide prompt: please put your facebook PAGE Link  

  - Facebook Likes  
    - Price per 1000 Likes: $3.49
    - Guide prompt: please put your facebook POST Link  

  - Facebook Comments   
    - Price per 1000 Comments: $5.49
    - Guide prompt: please put your facebook POST Link  

  ## Instagram Services:
  - Instagram Followers  
    - Price per 1000 Views: $14.99
    - Guide prompt: please put your instagram ACCOUNT Link  

  - Instagram Views  
    - Price per 1000 Views: $3.99
    - Guide prompt: please put your instagram VIDEO Link  

  - Instagram Comments
    - Price per 1000 Views: $7.49
    - Guide prompt: please put your instagram POST Link  

  - Instagram Likes
    - Price per 1000 Views: $8.49
    - Guide prompt: please put your instagram POST Link  


  ## TikTok Services:
  - TikTok Followers 
    - Price per 1000 Views: $9.49
    - Guide prompt: please put your tiktok ACCOUNT Link  

  - TikTok Views  
    - Price per 1000 Views: $3.49
    - Guide prompt: please put your tiktok VIDEO Link  

  -TikTok Likes
    - Price per 1000 Views: $2.99
    - Guide prompt: please put your tiktok POST Link  

  ## Twitter Services:
  - Twitter Followers   
    - Price per 1000 Views: $11.49
    - Guide prompt: please put your twitter ACCOUNT Link  

  - Twitter Views   
    - Price per 1000 Views: $5.99
    - Guide prompt: please put your twitter VIDEO Link  

  - Twitter Comments
    - Price per 1000 Views: $7.49
    - Guide prompt: please put your twitter POST Link  

  - Twitter Likes
    - Price per 1000 Views: $8.99
    - Guide prompt: please put your twitter POST Link  
'''
context = [
  {'role': 'system',
  'content': f"""
        You are ShopBot, an AI assistant for my online bi3 Smart . 
        Your role is to assist customers in browsing services, providing information, and guiding them through the checkout process. 
        Be friendly and helpful in your interactions.
        We offer a variety of services across categories such as Instagram Services, Facebook Services, TikTok Services, YouTube Services. 
        Feel free to ask customers about their preferences, recommend services, and inform them about any ongoing services.
        The Current Product List is limited as below:
        ```{product_list}```
        Make the shopping experience enjoyable and encourage customers to reach out if they have any questions or need assistance."""}]

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        response = get_completion_from_messages(context + [{'role': 'user', 'content': user_input}])
        return JsonResponse({'bot_response': response})
    else:
        return render(request, 'chatbot.html')
