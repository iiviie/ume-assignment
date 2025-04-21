import google.generativeai as genai
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuerySerializer, AnalysisResponseSerializer
from .models import QueryLog

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-lite')

ACTIONS = {
    'ORDER_FOOD': {
        'action_code': 'ORDER_FOOD',
        'display_text': 'Order Food Online'
    },
    'FIND_RECIPE': {
        'action_code': 'FIND_RECIPE',
        'display_text': 'Find Recipes'
    },
    'ASK_HELP': {
        'action_code': 'ASK_HELP',
        'display_text': 'Get Help'
    },
    'SHARE_NEWS': {
        'action_code': 'SHARE_NEWS',
        'display_text': 'Share News'
    },
    'SCHEDULE_MEETING': {
        'action_code': 'SCHEDULE_MEETING',
        'display_text': 'Schedule a Meeting'
    },
    'SEARCH_INFO': {
        'action_code': 'SEARCH_INFO',
        'display_text': 'Search for Information'
    }
}

class AnalyzeView(APIView):
    def get_suggested_actions(self, tone, intent, query):
        """
        Select appropriate actions based on tone, intent, and query text.
        Returns 1-3 relevant actions.
        """
        suggested_actions = []
        
        intent = intent.lower()
        query = query.lower()
        
        if ('order' in intent or 'purchase' in intent or 'buy' in intent or 
            'order' in query or 'purchase' in query or 'buy' in query):
            suggested_actions.append(ACTIONS['ORDER_FOOD'])
        elif ('recipe' in intent or 'cook' in intent or 'food' in intent or 
              'recipe' in query or 'cook' in query or 'food' in query):
            suggested_actions.append(ACTIONS['FIND_RECIPE'])
        elif ('help' in intent or 'question' in intent or 'assist' in intent or 
              'help' in query or 'question' in query or 'assist' in query):
            suggested_actions.append(ACTIONS['ASK_HELP'])
        elif ('news' in intent or 'update' in intent or 'information' in intent or 
              'news' in query or 'update' in query or 'information' in query):
            suggested_actions.append(ACTIONS['SHARE_NEWS'])
        elif ('meeting' in intent or 'schedule' in intent or 'appointment' in intent or 
              'meeting' in query or 'schedule' in query or 'appointment' in query):
            suggested_actions.append(ACTIONS['SCHEDULE_MEETING'])
        elif ('search' in intent or 'find' in intent or 'look' in intent or 
              'search' in query or 'find' in query or 'look' in query):
            suggested_actions.append(ACTIONS['SEARCH_INFO'])

        if not suggested_actions:
            suggested_actions.append(ACTIONS['SEARCH_INFO'])

        return suggested_actions[:3]

    def post(self, request):
        serializer = QuerySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        query = serializer.validated_data['query']

        try:
            prompt = f"""
            Analyze the following message and identify its tone and intent.
            Message: "{query}"
            
            Please respond in the following format only:
            {{"tone": "identified_tone", "intent": "identified_intent"}}
            
            Keep the tone and intent simple and single-worded where possible.
            """

            response = model.generate_content(prompt)
            analysis = eval(response.text)

            suggested_actions = self.get_suggested_actions(
                analysis['tone'],
                analysis['intent'],
                query
            )

            response_data = {
                'query': query,
                'analysis': analysis,
                'suggested_actions': suggested_actions
            }

            QueryLog.objects.create(
                query=query,
                tone=analysis['tone'],
                intent=analysis['intent'],
                suggested_actions=suggested_actions
            )

            response_serializer = AnalysisResponseSerializer(response_data)
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': 'Failed to process request', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )