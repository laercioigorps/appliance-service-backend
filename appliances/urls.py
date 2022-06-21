from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "appliances"

urlpatterns = [
    path("", views.ApplianceListView.as_view(), name="appliance_list"),
    path("brands/", views.BrandListView.as_view(), name="brand_list"),
    path("category/", views.CategoryListView.as_view(), name="category_list"),
    path("solutions/", views.SolutionListView.as_view(), name="solution_list"),
    path("problems/", views.ProblemListView.as_view(), name="problem_list"),
    path("symptoms/", views.SymptomListView.as_view(), name="symptom_list"),
    path("historics/", views.HistoricListView.as_view(), name="historic_list"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
