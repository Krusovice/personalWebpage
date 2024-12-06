from django.urls import path

from literature.views import literature_index, literature_detail, literature_delete, literature_upload


app_name = 'literature'
urlpatterns = [
    path('', literature_index, name='literature-index'),
    path('<int:item_id>/', literature_detail, name='literature-detail'),
    path('<int:item_id>/delete/', literature_delete, name='literature-delete'),
    path('upload/', literature_upload, name='literature-upload'),
]