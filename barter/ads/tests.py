from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Ad, ExchangeProposal


class AdModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем пользователя для тестирования
        cls.user = User.objects.create_user(username='testuser', password='12345')

    def test_ad_creation(self):
        # Тест создания объявления
        ad = Ad.objects.create(
            user=self.user,
            title="Тестовое объявление",
            description="Это тестовое описание.",
            category="Тестовая категория",
            condition="new"
        )
        self.assertEqual(ad.title, "Тестовое объявление")
        self.assertEqual(ad.description, "Это тестовое описание.")
        self.assertEqual(ad.category, "Тестовая категория")
        self.assertEqual(ad.condition, "new")

    def test_ad_str_method(self):
        # Тест метода __str__
        ad = Ad.objects.create(
            user=self.user,
            title="Тестовое объявление",
            description="Описание",
            category="Категория",
            condition="used"
        )
        self.assertEqual(str(ad), "Тестовое объявление")

    def test_ad_fields_validation(self):
        # Тест валидации заголовка (не может быть пустым)
        ad = Ad(
            user=self.user,
            title="",  # Пустой заголовок
            description="Описание",
            category="Категория",
            condition="new"
        )
        with self.assertRaises(ValidationError) as context:
            ad.full_clean()
        self.assertIn('title', context.exception.error_dict)

        # Тест валидации поля condition (некорректное значение)
        ad = Ad(
            user=self.user,
            title="Заголовок",
            description="Описание",
            category="Категория",
            condition="invalid_choice"  # Некорректное значение
        )
        with self.assertRaises(ValidationError) as context:
            ad.full_clean()
        self.assertIn('condition', context.exception.error_dict)


class ExchangeProposalModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем пользователей
        cls.user1 = User.objects.create_user(username='user1', password='12345')
        cls.user2 = User.objects.create_user(username='user2', password='12345')

        # Создаем объявления
        cls.ad_sender = Ad.objects.create(
            user=cls.user1,
            title="Отправитель",
            description="Описание отправителя",
            category="Категория",
            condition="new"
        )
        cls.ad_receiver = Ad.objects.create(
            user=cls.user2,
            title="Получатель",
            description="Описание получателя",
            category="Категория",
            condition="used"
        )

    def test_exchange_proposal_creation(self):
        # Тест создания предложения обмена
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad_sender,
            ad_receiver=self.ad_receiver,
            comment="Тестовый комментарий",
            status="pending"
        )
        self.assertEqual(proposal.comment, "Тестовый комментарий")
        self.assertEqual(proposal.status, "pending")

    def test_exchange_proposal_str_method(self):
        # Тест метода __str__
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad_sender,
            ad_receiver=self.ad_receiver,
            comment="Тестовый комментарий",
            status="pending"
        )
        expected_str = f"Предложение от {self.user1.username} к {self.user2.username}"
        self.assertEqual(str(proposal), expected_str)

    def test_exchange_proposal_fields_validation(self):
        # Тест валидации полей
        with self.assertRaises(Exception):
            # Попытка создать предложение без обязательных полей
            ExchangeProposal.objects.create(
                ad_sender=self.ad_sender,
                ad_receiver=None,  # Отсутствует получатель
                comment="Тестовый комментарий",
                status="pending"
            )

        with self.assertRaises(Exception):
            # Попытка создать предложение с некорректным значением поля status
            ExchangeProposal.objects.create(
                ad_sender=self.ad_sender,
                ad_receiver=self.ad_receiver,
                comment="Тестовый комментарий",
                status="invalid_status"  # Некорректное значение
            )


class AdListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем пользователя
        cls.user = User.objects.create_user(username='testuser', password='12345')

        # Создаем несколько объявлений
        Ad.objects.create(
            user=cls.user,
            title="Объявление 1",
            description="Описание 1",
            category="Категория 1",
            condition="new"
        )
        Ad.objects.create(
            user=cls.user,
            title="Объявление 2",
            description="Описание 2",
            category="Категория 2",
            condition="used"
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('ad_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('ad_list'))
        self.assertTemplateUsed(response, 'ads/ad_list.html')

    def test_pagination_is_four(self):
        response = self.client.get(reverse('ad_list'))
        self.assertEqual(len(response.context['ads']), 2)  # Проверяем количество объявлений на странице
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == (len(response.context['ads']) > 4))

    def test_search_filter(self):
        response = self.client.get(reverse('ad_list') + '?query=Объявление')
        self.assertEqual(len(response.context['ads']), 2)  # Оба объявления содержат слово "Объявление"

        response = self.client.get(reverse('ad_list') + '?query=Объявление+1')
        self.assertEqual(len(response.context['ads']), 1)  # Только одно объявление содержит "Объявление 1"


class AdCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')

    def setUp(self):
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('create_ad'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('create_ad'))
        self.assertTemplateUsed(response, 'ads/create_ad.html')

    def test_create_ad_with_valid_data(self):
        response = self.client.post(reverse('create_ad'), {
            'title': 'Новое объявление',
            'description': 'Описание нового объявления',
            'category': 'Категория',
            'condition': 'new'
        })
        self.assertEqual(response.status_code, 302)  # Перенаправление после успешного создания
        self.assertEqual(Ad.objects.count(), 1)  # Должно быть создано одно объявление

    def test_create_ad_with_invalid_data(self):
        response = self.client.post(reverse('create_ad'), {
            'title': '',  # Пустой заголовок
            'description': 'Описание',
            'category': 'Категория',
            'condition': 'new'
        })
        self.assertEqual(response.status_code, 200)  # Ошибка валидации, форма не отправлена
        self.assertEqual(Ad.objects.count(), 0)  # Объявление не должно быть создано


class AdDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.ad = Ad.objects.create(
            user=cls.user,
            title="Объявление 1",
            description="Описание 1",
            category="Категория 1",
            condition="new"
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/{self.ad.id}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('ad_detail', args=[self.ad.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('ad_detail', args=[self.ad.id]))
        self.assertTemplateUsed(response, 'ads/ad_detail.html')

    def test_context_contains_ad(self):
        response = self.client.get(reverse('ad_detail', args=[self.ad.id]))
        self.assertEqual(response.context['ad'], self.ad)


class AdUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.ad = Ad.objects.create(
            user=cls.user,
            title="Объявление 1",
            description="Описание 1",
            category="Категория 1",
            condition="new"
        )

    def setUp(self):
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/{self.ad.id}/edit/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('edit_ad', args=[self.ad.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('edit_ad', args=[self.ad.id]))
        self.assertTemplateUsed(response, 'ads/edit_ad.html')

    def test_update_ad_with_valid_data(self):
        response = self.client.post(reverse('edit_ad', args=[self.ad.id]), {
            'title': 'Обновленное объявление',
            'description': 'Обновленное описание',
            'category': 'Категория',
            'condition': 'used'
        })
        self.assertEqual(response.status_code, 302)  # Перенаправление после успешного обновления
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, 'Обновленное объявление')

    def test_update_ad_with_invalid_data(self):
        response = self.client.post(reverse('edit_ad', args=[self.ad.id]), {
            'title': '',  # Пустой заголовок
            'description': 'Описание',
            'category': 'Категория',
            'condition': 'new'
        })
        self.assertEqual(response.status_code, 200)  # Ошибка валидации, форма не отправлена
        self.ad.refresh_from_db()
        self.assertNotEqual(self.ad.title, '')  # Заголовок не должен измениться