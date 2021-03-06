from django.urls import include, re_path
from django.contrib import admin; admin.autodiscover()
from django.conf import settings
from django.views.generic import TemplateView
from django.views import static

urlpatterns = [
    # Just a simple example "home" page to show a bit of help/info.
    re_path(r'^$', TemplateView.as_view(template_name="home.html")),
    
    # This is the URLconf line you'd put in a real app to include the FAQ views.
    re_path(r'^faq/', include('fack.urls')),
    
    # Everybody wants an admin to wind a piece of string around.
    re_path(r'^admin/', admin.site.urls),

    # Normally we'd do this if DEBUG only, but this is just an example app.
    re_path(
        r'^static/(?P<path>.*)$',
        static.serve,
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}
    ),
]
