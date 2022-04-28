from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('livepoll/', include('livepoll.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

"""
admin/
[name='redirect']
homepage/ [name='homepage']
profile/<slug:username> [name='profile']
post-delete/<int:pk> [name='post_delete']
posts/ [name='post_titles']
post/<int:pk>/ [name='post_detail']
post/new/ [name='post_new']
post/<int:pk>/edit/ [name='post_edit']
create-account/ [name='create_account']
accounts/ login/ [name='login']
accounts/ logout/ [name='logout']
accounts/ password_change/ [name='password_change']
accounts/ password_change/done/ [name='password_change_done']
accounts/ password_reset/ [name='password_reset']
accounts/ password_reset/done/ [name='password_reset_done']
accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/ reset/done/ [name='password_reset_complete']
"""
