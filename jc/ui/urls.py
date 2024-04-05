from django.urls import path
from ui import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('query', views.QueryView.as_view(), name="query"),

    path('indices', views.IndexListView.as_view(), name="index-list"),
    path('indices/<str:key>', views.IndexDetailView.as_view(), name="index-detail"),
    path('vectors', views.VectorListView.as_view(), name="vector-list"),
    path('vectors/<str:id>', views.VectorDetailView.as_view(), name="vector-detail"),
    path('documents', views.DocumentListView.as_view(), name="document-list"),
    path('documents/<uuid:uuid>', views.DocumentDetailView.as_view(), name="document-detail"),
    path('knowledge-graph', views.KnowledgeGraphView.as_view(), name="knowledge-graph"),
    path('knowledge-graph/graph', views.KnowledgeGraphGraphView.as_view(), name="knowledge-graph-graph"),

    path('provider', views.ProviderListView.as_view(), name="provider-list"),
    path('flavor', views.FlavorListView.as_view(), name="flavor-list"),
]
