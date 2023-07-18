from rest_framework.decorators import api_view
from rest_framework.response import Response
from bangazonapi.models import User

@api_view(['POST'])
def check_user(request):

    uid = request.data['uid']

    user = User.objects.filter(uid=uid).first()
    
    if user is not None:
      data ={
        'id': user.id,
        'uid': user.uid,
        'email': user.email,
        'url': user.url,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username
      }
      return Response(data)
    else:
      data = {'valid': False}
      return Response(data)

@api_view(['POST'])
def register_user(request):
  
  user = User.objects.create(
    uid = request.data['uid'],
    email = request.data['email'],
    url = request.data['url'],
    first_name = request.data['first_name'],
    last_name = request.data['last_name'],
    username = request.data['username']
    )
  
  data = {
    'id': user.id,
    'uid': user.uid,
    'email': user.email,
    'url': user.url,
    'first_name': user.first_name,
    'last_name': user.last_name,
    'username': user.username
  }
  return Response(data)
