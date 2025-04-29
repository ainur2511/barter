from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import AdListView, AdCreateView, AdDetailView, AdUpdateView, AdDeleteView, CreateExchangeProposalView, \
    UpdateExchangeProposalStatusView, ExchangeProposalListView, CustomLoginView, RegisterView, CustomLogoutView

urlpatterns = [
    # Главная страница (список объявлений)
    path('', AdListView.as_view(), name='ad_list'),  # Список объявлений
    path('create/', AdCreateView.as_view(), name='create_ad'),  # Создание объявления
    path('<int:pk>/', AdDetailView.as_view(), name='ad_detail'),  # Детали объявления
    path('<int:pk>/edit/', AdUpdateView.as_view(), name='edit_ad'),  # Редактирование объявления
    path('<int:pk>/delete/', AdDeleteView.as_view(), name='delete_ad'),  # Удаление объявления

    # CRUD для предложений по обмену
    path('create/<int:ad_receiver_id>/', CreateExchangeProposalView.as_view(), name='create_exchange_proposal'),
    path('update/<int:pk>/', UpdateExchangeProposalStatusView.as_view(), name='update_exchange_proposal_status'),
    path('proposals/', ExchangeProposalListView.as_view(), name='exchange_proposals'),

    # Авторизация
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # Регистрация
    path('register/', RegisterView.as_view(), name='register'),
]
