from django.contrib import admin
from django.urls import include, path
from config.utils.error_handler import hadler404, hadler500


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('account.urls')),
    path('api/', include('student.urls')),
       path('api/', include('todoList.urls')),
]


handler404 = hadler404
handler500 = hadler500

