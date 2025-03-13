
from django.contrib import admin
from django.urls import path,include
from tickets import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


router=DefaultRouter()
router.register('guests',views.Viewsets_guests)
router.register('movies',views.Viewsets_movies)
router.register('reservations',views.Viewsets_reservations)

urlpatterns = [
    path('admin/', admin.site.urls),
    #1
    path('django/jsonresponsenomodle/',views.no_rest_no_model),
    #2
    path('django/jsonresponsefrommodle/',views.no_rest_from_model),
    #3 GET POST frame restframework function based views view @api_view
    path('rest/fbv/',views.FBV_list),
    #3.1 GET PUT DELETE
    path('rest/FBV_PK/<int:pk>/',views.FBV_PK),
    #4.1 GET POST form restframework class based views API
    path('rest/cbv/',views.CBV_list.as_view()),
    #4.2 GET PUT DELETE  rest framework class based views APIView
    path('rest/cbv/<int:pk>/',views.CBV_PK.as_view()),
    #5.1 GET POST form restframework class based views mixins
    path('rest/mixins/',views.mixins_list.as_view()),
    #5.2 GET PUT DELETE  rest framework class based mixins
    path('rest/mixins/<int:pk>/',views.mixins_pk.as_view()),
    #6.1 GET POST form restframework class based views generics
    path('rest/generics/',views.generics_list.as_view()),
    #6.2 GET PUT DELETE  rest framework class based generics
    path('rest/generics/<int:pk>/',views.generics_list_pk.as_view()),
    #7 viewsets
    path('rest/viewsets/',include(router.urls)),
    #8 fiend movie
    path('fbv/findmovie/',views.find_movie),
    #9 new reservation
    path('fbv/newreservation/',views.new_reservation),
    #10 rest auth url 
    path('api-auth/',include('rest_framework.urls')),#login logout
    #11 token authentication  display the authtoken in admin view 
    path('api-token-auth/',obtain_auth_token),
    #12 post pk generics

    path('post/generics/<int:pk>/',views.post_pk.as_view()),
]
