"""
URL configuration for swtp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from webapp.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('horspool/', horspool_view, name='horspool'),
    path('', base_view, name='base'),
    path('dotplot/', dotplot_view, name='dotplot'),
    path('simple_search/', simple_search_view, name='simple_search'),
    path('overlap/', overlap_view, name='overlap'),
    path('needleman_wunsch/', needleman_wunsch_view, name='needleman_wunsch'),
    path('smith_waterman/', smith_waterman_view, name='smith_waterman'),
    path('upgma/', upgma_view, name='upgma'),
    path('neighbour_joining/', neighbour_joining_view, name='neighbour_joining'),
    path('suffix_tree/', suffix_tree_view, name='suffix_tree'),
    path('suffix_trie/', suffix_trie_view, name='suffix_trie'),
    path('suffix_array/', suffix_array_view, name='suffix_array'),
    path('glocal_alignment/', glocal_alignment_view, name='glocal_alignment'),
]


