import datetime
import json

from knox.auth import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from visitors.decorators import user_is_visitor

import Scanner.main as scn
from SmartLLock.settings import QR_TTL
from .logic import isValid

from .serializers import RegisterSerializer


@api_view(['POST'])
def login_api(request):
    # data validation and serializing
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']

    # create token
    created, token = AuthToken.objects.create(user)
    if created is None:
        print('Token creation failed')

    return Response({
        'user_info': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        },
        'token': token
    })


@api_view(['POST'])
def register_api(request):
    # data validation and serializing
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    # create token
    _, token = AuthToken.objects.create(user)

    return Response({
        'user_info': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        },
        'token': token
    })


@api_view(['GET'])
def get_user_data(request):
    user = request.user

    if user.is_authenticated:
        return Response({
            'user_info': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
        }
        )
    return Response({'error': 'not authenticated'}, status=400)


@api_view(['GET'])
def get_QR(request):
    user = request.user

    if user.is_authenticated:
        data, code = scn.generate_QR()
        headers = {'Cache-Control': f"max-age={QR_TTL}"}
        request.session['Datetime'] = datetime.datetime.now().isoformat()
        request.session['Code'] = code
        return Response(data=data, headers=headers, content_type="image/png", status=200)

    return Response({'error': 'not authenticated'}, status=400)

@user_is_visitor(scope="foo")
@api_view(['GET'])
def get_QR_guest(request):
    data, code = scn.generate_QR()
    headers = {'Cache-Control': f"max-age={QR_TTL}"}
    request.session['Datetime'] = datetime.datetime.now().isoformat()
    request.session['Code'] = code
    return Response(data=data, headers=headers, content_type="image/png", status=200)

@api_view(['GET'])
def get_visitor_link(request):

    pass

@api_view(['POST'])
def validate(request):
    json_data = json.loads(request.body)
    code = json_data['Code']

    if isValid(code):
        return Response(status=200)

    return Response(status=404)
