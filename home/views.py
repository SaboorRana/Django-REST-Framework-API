from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Person
from .serializers import PersonSerializer, LoginSerializer, RegisterSerializer
from rest_framework import viewsets
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action


@api_view(['GET','POST'])
def index(request):
    data = {
        'title': 'Home',
        'description': 'Welcome to the home page.'
    }
    if request.method=='GET':
        print(request.GET.get('search', 'No name provided'))
        data['message'] = 'This is a GET request.'
    elif request.method=='POST':
        val = request.data
        print('*****')
        print(val)
        data['message'] = 'This is a POST request.'
    return Response(data) 

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            data = serializer.validated_data
            print(data)
            return Response({'message': 'Login successful', 'data': data})
        return Response(serializer.errors, status=400)

from django.core.paginator import Paginator

class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated to access this view
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        print(request.user)
        objs = Person.objects.all()
        page = request.GET.get('page', 1)
        page_size = 3
        paginator = Paginator(objs, page_size)
        try:
            pg = paginator.page(page)
        except Exception as e:
            return Response({
                'error':'Invalid page number'
            })
        serializer =  PersonSerializer(pg, many=True)
        return Response(serializer.data)
        return Response({'message': 'This is a GET request for Person'})
    def post(self, request):
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': 'This is a POST request for Person'})
    def put(self, request):
        person_id = request.data.get('id')
        if not person_id:
            return Response({'error': 'ID is required for PUT request'}, status=400)
        instance = get_object_or_404(Person, id=person_id)
        serializer = PersonSerializer(instance,data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response({'message': 'This is a PUT request for Person'})
    def patch(self, request):
        person_id = request.data.get('id')
        if not person_id:
            return Response({'error': 'ID is required for PUT request'}, status=400)
        instance = get_object_or_404(Person, id=person_id)
        serializer = PersonSerializer(instance,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': 'This is a PATCH request for Person'})
    def delete(self, request):
        person_id = request.get('id')
        if not person.id:
            return Response({'error': 'ID is required for DELETE request'}, status=400)
        instance = get_object_or_404(Person, id=person_id)
        instance.delete()
        return Response({'message': 'This is a DELETE request for Person'})
    
@api_view(['GET','POST','PUT', 'PATCH'])
def person(request):
    if request.method=='GET':
        objs = Person.objects.filter(color__isnull=False)
        serializer =  PersonSerializer(objs, many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method in ['PUT','PATCH']:
        person_id = request.data.get('id')
        if not person_id:
            return Response({'error': 'ID is required for PUT request'}, status=400)
        instance = get_object_or_404(Person, id=person_id)
        serializer = PersonSerializer(instance,data=request.data, partial=(request.method=='PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    
class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    http_method_names = ['get', 'post']
    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name_startswith = search)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data':serializer.data},status = status.HTTP_207_MULTI_STATUS)
    
    @action(detail=True, methods=['post'])
    def send_email(self, request, pk):
        person = Person.objects.get(pk=pk)
        serializer = PersonSerializer(person)
        return Response({
            'status': True,
            'message': 'Email sent successfully!',
            'data': serializer.data
            })

class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer  = RegisterSerializer(data= data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response({
            'status': True,
            'message': 'User registered successfully',
            'data':serializer.data,
        }, status=status.HTTP_201_CREATED
        )

class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)

        # Validate the input data
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Check if a user with the given email exists
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'status': False,
                'message': 'User does not exist'
            }, status=status.HTTP_404_NOT_FOUND)

        # Authenticate using username (since Django authenticate uses 'username' by default)
        user = authenticate(username=user_obj.username, password=password)

        # Check if credentials are valid
        if user is None:
            return Response({
                'status': False,
                'message': 'Invalid email or password'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Create or get a token for the authenticated user
        token, _ = Token.objects.get_or_create(user=user)

        # Return success response with token
        return Response({
            'status': True,
            'message': 'Login Successful',
            'token': str(token)
        }, status=status.HTTP_200_OK)  # ✔ Use 200 for login instead of 201 (201 = resource created)

