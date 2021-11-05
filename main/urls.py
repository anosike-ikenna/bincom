from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r"^$", views.home_page, name="home_page"),
    re_path(r"^question1/$", views.question_one, name="question_one"),
    re_path(r"^question2/$", views.question_two, name="question_two"),
    re_path(r"^question3/$", views.question_three, name="question_three"),
    re_path(r"^question3a/$", views.question_three_a, name="question_three_a"),
    re_path(r"^question3b/$", views.question_three_b, name="question_three_b"),
    re_path(
        r"^question3b/(?P<pu_u_id>\d+)/add_results/$", 
        views.add_results, 
        name="add_results"
    ),
    re_path(r"^pu/(?P<id>\d+)/$", views.polling_unit_detail, name="pu_detail"),
    re_path(r"^pu/(?P<id>\d+)/delete$", views.polling_unit_delete, name="pu_delete"),
    re_path(r"^lga/(?P<id>\d+)/result/$", views.lga_result, name="lga_result"),
    re_path(r"^api/lga/(?P<lga_id>\d+)/ward/$", views.wards_list),
    re_path(r"^api/ward/(?P<uward_id>\d+)/pu/$", views.pu_list),
    # re_path(r"^api/pu/(?P<name>\w+)/pu/$", views.pu_exists),
]