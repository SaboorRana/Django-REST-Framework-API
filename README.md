A complete example project demonstrating how to build RESTful APIs using Django REST Framework, with features like:

🔐 Token Authentication

🔄 ModelViewSets with custom @actions

📄 Serializers

📄 API Pagination

✅ Class-based views using APIView

👤 User registration & login API

🚀 Features Overview
✅ Models
Person model with fields like:

class Person(models.Model):
    name = models.CharField(...)
    email = models.EmailField(...)
    is_active = models.BooleanField(default=True)
    color = models.CharField(...) 
    
🔧 Serializers

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
Used to convert model instances into JSON and validate input data.

🔄 ViewSets & Routers

class PeopleViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
Auto-generates routes like:

GET /api/people/

POST /api/people/

GET /api/people/<id>/

⚙️ Custom Actions with @action

@action(detail=False, methods=['get'])
def active(self, request):
    return Response(...)  # List active people

@action(detail=True, methods=['post'])
def deactivate(self, request, pk=None):
    return Response(...)  # Deactivate person

@action(detail=False, methods=['post'])
def send_email(self, request):
    return Response(...)  # Simulate email sending
Accessible via:

/api/people/active/

/api/people/<id>/deactivate/

/api/people/send_email/

🔒 Authentication

Token-based auth using TokenAuthentication
Protected views like PersonAPI using IsAuthenticated

📄 Pagination (Manual)

from django.core.paginator import Paginator
def get(self, request):
    objs = Person.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(objs, 3)
    page_obj = paginator.page(page)
    ...
Returns paginated results like:
{
  "count": 10,
  "total_pages": 4,
  "current_page": 1,
  "results": [...]
}

🔗 URL Configuration

router.register(r'people', PeopleViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', RegisterAPI.as_view()),
    path('api/login/', LoginAPI.as_view()),
    path('api/personAPI/', PersonAPI.as_view()),
]
📬 Example Endpoints
Method	Endpoint	Description
GET	/api/people/	List all people
GET	/api/people/active/	List only active people
POST	/api/people/<id>/deactivate/	Deactivate a person
POST	/api/people/send_email/	Simulate sending email
POST	/api/register/	Register a new user
POST	/api/login/	Log in and receive token
GET	/api/personAPI/?page=1	Paginated list of people (protected)

