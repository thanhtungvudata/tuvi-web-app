from django.contrib.auth import views as auth_views
from django.urls import re_path

from apps.tuvi.views import (
    api, lasotuvi_new_index, lasotuvi_new_result, lasotuvi_new_manage,
    save_laso, update_laso, get_lasos, get_laso_detail, get_folders,
    delete_laso, delete_folder, toggle_favorite_laso, move_laso, register_view,
    create_folder
)

urlpatterns = [
    # Authentication URLs
    re_path(r'^register/$', register_view, name='register'),
    re_path(r'^login/$', auth_views.LoginView.as_view(template_name='tuvi/login.html'), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # API URLs
    re_path(r'^api$', api, name='lasotuvi_api'),
    re_path(r'^api/save-laso/$', save_laso, name='save_laso'),
    re_path(r'^api/update-laso/$', update_laso, name='update_laso'),
    re_path(r'^api/lasos/$', get_lasos, name='get_lasos'),
    re_path(r'^api/laso/(?P<laso_id>\d+)/$', get_laso_detail, name='get_laso_detail'),
    re_path(r'^api/laso/(?P<laso_id>\d+)/delete/$', delete_laso, name='delete_laso'),
    re_path(r'^api/laso/(?P<laso_id>\d+)/toggle-favorite/$', toggle_favorite_laso, name='toggle_favorite_laso'),
    re_path(r'^api/laso/(?P<laso_id>\d+)/move/$', move_laso, name='move_laso'),
    re_path(r'^api/folders/$', get_folders, name='get_folders'),
    re_path(r'^api/folder/create/$', create_folder, name='create_folder'),
    re_path(r'^api/folder/(?P<folder_id>\d+)/delete/$', delete_folder, name='delete_folder'),
    re_path(r'^result/$', lasotuvi_new_result, name='lasotuvi_result'),
    re_path(r'^new/$', lasotuvi_new_index, name='lasotuvi_new'),
    re_path(r'^$', lasotuvi_new_manage, name='lasotuvi_index'),
]