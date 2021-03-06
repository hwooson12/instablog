"""웹서비스개발캠프 5기 6주차 과제 tests.py (instablog용)
instablog 프로젝트의 blog 앱 디렉터리에 넣고 테스트를 수행하세요.

테스트를 skip 처리 해놨으므로
    @unittest.skip('이 장식자를 제거하며 하나씩 테스트를 통과하세요')
이 장식자를 제거하며 테스트를 수행해야 합니다.

기존에 작성하신 tests.py 파일을 덮어쓰지 않게 백업하세요.
URL name이나 View 함수 이름은 본 테스트 파일 내용을 참고해서 맞추시면 됩니다.
"""
import unittest
from collections import namedtuple

from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve

from . import views, models, forms


User = get_user_model()  # noqa


class PostTest(TestCase):
    def setUp(self):
        """본 테스트에 공통으로 사용하는 데이터들.
        test users를 만들고 이 이용자가 접근한다는 전제로 사용함.
        """
        self.client = Client()
        self.users = (
            {'username': 'test1', 'password': '12345678'},
            {'username': 'test2', 'password': '12345678'},
        )
        for _user in self.users:
            User.objects.create_user(**_user)

        self.urls = namedtuple('URL', (
            'create_post', 'delete_post', 'view_post', 'list_posts',
            'create_comment', 'delete_comment',
        ))(
            # 게시물 작성하는 URL name 은 'create_post'
            lambda : reverse('create_post'),

            # 개별 게시물 지우는 URL name 은 'delete_post'이며,
            # URL패턴의 그룹은 pk.
            lambda pk: reverse('delete_post', kwargs={'pk': pk}),

            # 개별 게시물 보는 URL name 은 'view_post'이며,
            # URL패턴의 그룹은 pk.
            lambda pk: reverse('view_post', kwargs={'pk': pk}),

            # 게시물 목록 URL name 은 'list_posts'
            lambda : reverse('list_posts'),

            # 댓글 다는 URL name 은 'create_comment'이며,
            # URL패턴의 그룹은 게시물의 pk.
            lambda pk: reverse('create_comment', kwargs={'pk': pk}),

            # 댓글 지우는는 URL name 은 'delete_comment이며,
            # URL패턴의 그룹은 댓글의 pk.
            lambda pk: reverse('delete_comment', kwargs={'pk': pk}),
        )

        self.category = models.Category(name='New Category')
        self.category.save()

    def _login(self, username, password):
        # 로그인 시도.
        return self.client.post(
            settings.LOGIN_URL, {'username': username, 'password': password}
        )

    def _add_post(self, data, follow=True):
        # 게시물 게시 시도.
        return self.client.post(
            self.urls.create_post(), data=data, follow=follow
        )

    # @unittest.skip('이 장식자를 제거하며 하나씩 테스트를 통과하세요')
    def test_404(self):
        """없는 페이지에 접근하는 테스트.
        """
        response = self.client.get('/page_not_found/')
        self.assertEqual(response.status_code, 404)

    # @unittest.skip('이 장식자를 제거하며 하나씩 테스트를 통과하세요')
    def test_create_post_by_view_on_logout(self):
        """로그아웃 상태에서 뷰 함수를 이용해 게시물을 게시하는 테스트.
        """
        _form_data = {
            'category': self.category.pk,
            'title': 'test title',
            'content': 'test content',
        }
        # 로그인하지 않은 상태에서 게시물 게시 시도.
        response = self._add_post(_form_data)

        # 로그인 하지 않았으므로 로그인 URL로 redirect 됐는지 확인.
        self.assertEqual(response.resolver_match.func.__name__, 'login')
        self.assertEqual(response.redirect_chain[0][1], 302)

    # @unittest.skip('이 장식자를 제거하며 하나씩 테스트를 통과하세요')
    def test_create_post_by_view_on_login(self):
        """로그인 상태에서 뷰 함수를 이용해 게시물을 게시하는 테스트.
        """
        _form_data = {
            'categories': self.category.pk,
            'title': 'Sjfdlkja23@#$!@SDF title',
            'content': 'FSAD@3@#$!sdflkj content',
        }
        self._login(**self.users[0])
        # 게시물 게시 시도.
        response = self._add_post(_form_data)
        # 가장 마지막에 등록된 게시물 데이터를 가져온다.
        latest_post = models.Post.objects.latest('pk')
        # 게시물 게시 후 해당 개별 게시물을 보는 URL로 redirect 했는지 확인.
        _view_post_url = self.urls.view_post(latest_post.pk)
        self.assertEqual(
            response.redirect_chain[0][0], _view_post_url
        )
        self.assertEqual(response.redirect_chain[0][1], 302)
        # 이동한 URL의 뷰 함수가 detail_post 인지 테스트.
        self.assertEqual(
            response.resolver_match.func,
            resolve(_view_post_url)[0]  # see also : https://goo.gl/htu8ko
        )

        # 저장한 게시물의 개별 보기 url로 접근
        response = self.client.get(_view_post_url)
        # 화면에 사용된 템플릿 컨텍스트의 post와 latest_post 의 pk 비교.
        self.assertEqual(
            response.context['post'].pk,
            latest_post.pk
        )
        # 화면에 사용된 템플릿 컨텍스트의 post와 글 작성에 사용한 제목 비교.
        self.assertEqual(
            response.context['post'].title,
            _form_data['title']
        )

    # @unittest.skip('이 장식자를 제거하며 하나씩 테스트를 통과하세요')
    def test_create_post_for_form_errors(self):
        """뷰 함수를 이용해 게시물을 게시하는 테스트 중 필수 입력 폼 테스트.
        """
        self._login(**self.users[0])

        # 필수 입력 항목인 category, title, content 빠뜨리고 게시물 게시 시도.
        response = self._add_post({})
        # 게시에 사용한 폼 인스턴스 객체가 템플릿 컨텍스트에 있는지 테스트.
        self.assertIn('form', response.context)
        # 템플릿 변수인 form에 필수 폼 필드에 대해 오류가 있는지 테스트.
        self.assertTrue(response.context['form'].has_error('categories'))
        self.assertTrue(response.context['form'].has_error('title'))
        self.assertTrue(response.context['form'].has_error('content'))

        # 필수 입력 항목인 title, content 빠뜨리고 게시물 게시 시도.
        _form_data = {}
        _form_data['categories'] = self.category.pk,
        response = self._add_post(_form_data)
        # 게시에 사용한 폼 인스턴스 객체가 템플릿 컨텍스트에 있는지 테스트.
        self.assertIn('form', response.context)
        # 템플릿 변수인 form에 필수 폼 필드에 대해 오류가 있는지 테스트.
        self.assertFalse(response.context['form'].has_error('categories'))
        self.assertTrue(response.context['form'].has_error('title'))
        self.assertTrue(response.context['form'].has_error('content'))

        # 필수 입력 항목인 content 빠뜨리고 게시물 게시 시도.
        _form_data['title'] = 'SADFSAFD#$!@#$! title'
        response = self._add_post(_form_data)
        # 게시에 사용한 폼 인스턴스 객체가 템플릿 컨텍스트에 있는지 테스트.
        self.assertIn('form', response.context)
        # 템플릿 변수인 form에 필수 폼 필드에 대해 오류가 있는지 테스트.
        self.assertFalse(response.context['form'].has_error('categories'))
        self.assertFalse(response.context['form'].has_error('title'))
        self.assertTrue(response.context['form'].has_error('content'))

        # 필수 입력 항목 다 넣고 게시물 게시 시도.
        _form_data['content'] = 'SADFSAFD#$!@#$! content'
        response = self._add_post(_form_data)
        # 게시에 사용한 폼 인스턴스 객체가 템플릿 컨텍스트에 없는지 테스트.
        self.assertNotIn('form', response.context) # 이해가 되질 않는다..

    # @unittest.skip('이 장식자를 제거하며 하나씩 테스트를 통과하세요')
    def test_view_post_not_exists(self):
        """존재하지 않는 개별 게시물 페이지에 접속하여 404가 뜨는지 테스트.
        """

        # 존재하지 않는 게시물에 접근.
        response = self.client.get(self.urls.view_post(9999), follow=True)
        # http status가 404인지 확인.
        self.assertEqual(response.status_code, 404)

    # @unittest.skip('이 장식자를 제거하며 하나씩 테스트를 통과하세요')
    def test_delete_post_on_logout(self):
        """로그아웃 상태에서 개별 게시물을 지우는 테스트.
        """
        _form_data = {
            'categories': self.category.pk,
            'title': 'Sjfdlkja23@#$!@SDF title',
            'content': 'FSAD@3@#$!sdflkj content',
        }
        self._login(**self.users[0])
        # 게시물 게시 시도.
        response = self._add_post(_form_data)
        self.assertIn(response.status_code, (200, 201,))
        latest_post = models.Post.objects.latest('pk')

        # test1 로그아웃
        self.client.get(settings.LOGOUT_URL)

        # 로그인하지 않고 삭제 url 접근
        response = self.client.get(
            self.urls.delete_post(latest_post.pk), follow=True
        )
        # 로그인 URL로 redirect 됐는지 확인.
        self.assertEqual(response.resolver_match.func.__name__, 'login')

    # @unittest.skip('이 장식자를 제거하며 하나씩 테스트를 통과하세요')
    def test_delete_post_without_permm(self):
        """권한 없이 개별 게시물을 지우는 시도하는 테스트.
        """
        _form_data = {
            'categories': self.category.pk,
            'title': 'Sjfdlkja23@#$!@SDF title',
            'content': 'FSAD@3@#$!sdflkj content',
        }
        self._login(**self.users[0])
        # 게시물 게시 시도.
        response = self._add_post(_form_data)
        self.assertIn(response.status_code, (200, 201,))
        latest_post = models.Post.objects.latest('pk')

        # test1 로그아웃
        self.client.get(settings.LOGOUT_URL)
        # test2 로그인
        self._login(**self.users[1])

        _delete_post_url = self.urls.delete_post(latest_post.pk)
        # http method POST로 접근.
        response = self.client.post(_delete_post_url, follow=True)
        # 권한이 없으므로 403 status 응답해야 함.
        self.assertEqual(response.status_code, 403)

    # @unittest.skip('이 장식자를 제거하며 하나씩 테스트를 통과하세요')
    def test_delete_post(self):
        """개별 게시물을 지우는 테스트.
        """
        _form_data = {
            'categories': self.category.pk,
            'title': 'Sjfdlkja23@#$!@SDF title',
            'content': 'FSAD@3@#$!sdflkj content',
        }
        self._login(**self.users[0])
        # 게시물 게시 시도.
        response = self._add_post(_form_data)
        self.assertIn(response.status_code, (200, 201,))
        latest_post = models.Post.objects.latest('pk')

        _delete_post_url = self.urls.delete_post(latest_post.pk)

        # http method GET으로 접근.
        response = self.client.get(_delete_post_url, follow=True)
        self.assertEqual(response.status_code, 200)
        # 이동한 URL의 뷰 함수가 delete_post 인지 테스트.
        self.assertEqual(
            response.resolver_match.func,
            resolve(_delete_post_url)[0]
        )

        # http method POST로 접근.
        response = self.client.post(_delete_post_url, follow=True)
        # 삭제 후 글 목록으로 이동했는지 확인
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(
            response.resolver_match.func,
            resolve(self.urls.list_posts())[0]
        )

        # 삭제한 게시물 url 접근 시 404인지.
        response = self.client.get(self.urls.view_post(latest_post.pk))
        self.assertEqual(response.status_code, 404)

        # DB에 삭제한 게시물이 존재하는 지 확인
        _exists = models.Post.objects.filter(pk=latest_post.pk).exists()
        self.assertFalse(_exists)
