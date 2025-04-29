from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Ad, ExchangeProposal
from .forms import AdForm, AdFilterForm, ExchangeProposalForm
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm


# Главная страница (список объявлений)
class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    ordering = ['-created_at']  # Сортировка по дате создания
    paginate_by = 4  # Пагинация

    def get_queryset(self):
        queryset = super().get_queryset()
        form = AdFilterForm(self.request.GET)

        if form.is_valid():
            query = form.cleaned_data.get('query')
            category = form.cleaned_data.get('category')
            condition = form.cleaned_data.get('condition')

            # Поиск по ключевым словам
            if query:
                queryset = queryset.filter(
                    Q(title__icontains=query) | Q(description__icontains=query)
                )

            # Фильтрация по категории
            if category:
                queryset = queryset.filter(category__icontains=category)

            # Фильтрация по состоянию
            if condition:
                queryset = queryset.filter(condition=condition)

        return queryset.order_by('-created_at')  # Сортировка по дате создания

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AdFilterForm(self.request.GET)
        return context

    def get_paginate_by(self, queryset):
        # Получаем значение paginate_by из GET-параметра или используем значение по умолчанию
        try:
            paginate_by = int(self.request.GET.get('paginate_by', self.paginate_by))
            if paginate_by in [5, 10, 20]:  # Разрешенные значения
                return paginate_by
        except ValueError:
            pass
        return self.paginate_by


# Детали объявления
class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'


# Создание объявления
class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/create_ad.html'
    success_url = reverse_lazy('ad_list')  # Перенаправление после создания

    def form_valid(self, form):
        form.instance.user = self.request.user  # Привязываем объявление к текущему пользователю
        messages.success(self.request, "Объявление успешно добавлено!")
        return super().form_valid(form)


class AdUpdateView(LoginRequiredMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/edit_ad.html'
    context_object_name = 'ad'

    def test_func(self):
        # Проверяем, является ли текущий пользователь автором объявления
        ad = self.get_object()
        return ad.user == self.request.user

    def handle_no_permission(self):
        # Если пользователь не имеет права редактировать, выводим сообщение об ошибке
        messages.error(self.request, "Вы не имеете права редактировать это объявление.")
        return redirect('ad_list')

    def get_success_url(self):
        # После успешного редактирования перенаправляем на страницу деталей объявления
        messages.success(self.request, "Объявление успешно обновлено!")
        return reverse_lazy('ad_detail', kwargs={'pk': self.object.id})


class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    context_object_name = 'ad'

    def test_func(self):
        # Проверяем, является ли текущий пользователь автором объявления
        ad = self.get_object()
        return ad.user == self.request.user

    def handle_no_permission(self):
        # Если пользователь не имеет права удалять, выводим сообщение об ошибке
        messages.error(self.request, "Вы не имеете права удалять это объявление.")
        return reverse_lazy('ad_list')

    def get_success_url(self):
        # После успешного удаления перенаправляем на страницу списка объявлений
        messages.success(self.request, "Объявление успешно удалено!")
        return reverse_lazy('ad_list')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        messages.success(self.request, "Вы успешно вошли в систему!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Неверное имя пользователя или пароль.")
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Вы вышли из системы.")
        return super().dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, "Вы успешно зарегистрировались! Теперь вы можете войти.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка регистрации. Пожалуйста, исправьте ошибки в форме.")
        return super().form_invalid(form)


# Создание предложения
class CreateExchangeProposalView(LoginRequiredMixin, CreateView):
    model = ExchangeProposal
    form_class = ExchangeProposalForm
    template_name = 'ads/exchange/create_proposal.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Передаем текущего пользователя в форму
        return kwargs

    def form_valid(self, form):
        ad_receiver_id = self.kwargs['ad_receiver_id']
        ad_receiver = Ad.objects.get(id=ad_receiver_id)

        form.instance.ad_receiver = ad_receiver
        messages.success(self.request, "Предложение обмена успешно отправлено!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('exchange_proposals')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_receiver'] = Ad.objects.get(id=self.kwargs['ad_receiver_id'])
        return context


# Обновление статуса предложения
class UpdateExchangeProposalStatusView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ExchangeProposal
    fields = ['status']
    template_name = 'ads/exchange/update_proposal_status.html'
    success_url = reverse_lazy('exchange_proposals')

    def test_func(self):
        proposal = self.get_object()
        return proposal.ad_receiver.user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "Вы не можете изменять статус своего предложения.")
        return redirect('exchange_proposals')

    def form_valid(self, form):
        messages.success(self.request, f"Статус предложения изменен на: {form.instance.get_status_display()}.")
        return super().form_valid(form)


# Просмотр предложений
class ExchangeProposalListView(LoginRequiredMixin, ListView):
    model = ExchangeProposal
    template_name = 'ads/exchange/exchange_proposals.html'
    context_object_name = 'proposals'

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_sender = self.request.GET.get('sender')
        filter_receiver = self.request.GET.get('receiver')
        filter_status = self.request.GET.get('status')

        queryset = queryset.filter(Q(ad_sender__user=self.request.user) | Q(ad_receiver__user=self.request.user))

        if filter_sender:
            queryset = queryset.filter(ad_sender__title__icontains=filter_sender)
        if filter_receiver:
            queryset = queryset.filter(ad_receiver__title__icontains=filter_receiver)
        if filter_status:
            queryset = queryset.filter(status=filter_status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_sender'] = self.request.GET.get('sender', '')
        context['filter_receiver'] = self.request.GET.get('receiver', '')
        context['filter_status'] = self.request.GET.get('status', '')
        return context




