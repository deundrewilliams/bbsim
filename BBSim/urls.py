"""BBSim URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from simulator.views import (
    get_all_contestants,
    get_single_game,
    create_game,
    sim_game,
    get_relationships,
)
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/contestants/", get_all_contestants),
    path("api/game/<int:id>", get_single_game),
    path("api/create-game", create_game),
    path("api/sim-game", sim_game),
    path("api/relationships/<int:id>", get_relationships),
    path("", TemplateView.as_view(template_name="index.html")),
]
