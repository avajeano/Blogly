from unittest import TestCase

from app import app
from models import db, User, Post, Tag

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bogly_test'

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Add sample user."""

        user = User(first_name="TestFirstName", last_name="TestLastName", image_url="https://img.freepik.com/free-vector/user-blue-gradient_78370-4692.jpg?w=826&t=st=1712240115~exp=1712240715~hmac=ec275943900481bfc64f790c547f043f8554bf3398e6cf2fab36de9dc3f590ce")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirstName', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.user_id}")
            self.assertEqual(resp.status_code, 200)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "TestFirstName2", "last_name": "TestLastName2", "image_url":"https://img.freepik.com/free-vector/user-blue-gradient_78370-4692.jpg?w=826&t=st=1712240115~exp=1712240715~hmac=ec275943900481bfc64f790c547f043f8554bf3398e6cf2fab36de9dc3f590ce"}
            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
    
    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete")
            deleted_user = User.query.get(self.user_id)

            self.assertIsNone(deleted_user)

class PostViewsTestCase(TestCase):
    """Tests posts for users."""

    def setUp(self):
        """Add sample post and user."""

        Post.query.delete()

        user = User(first_name="TestFirstName2", last_name="TestLastName2")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id 
        
        post = Post(title="TestTitle", content="TestContent", created_at="2024-04-07 22:57:15.356279", user_id=self.user_id)
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id 

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_posts(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestTitle', html)

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")

            self.assertEqual(resp.status_code, 200)

    def test_add_post(self):
        with app.test_client() as client:
            resp = client.get(f"users/{self.post_id}/posts_new")
            self.assertEqual(resp.status_code, 200)
    
    def test_edit_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}/edit")
            self.assertEqual(resp.status_code, 200)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post(f"posts/{self.post_id}/delete", follow_redirects=True)
            deleted_post = Post.query.get(self.post_id)
            self.assertIsNone(deleted_post)
            self.assertEqual(resp.status_code, 200)

class TagViewsTestCase(TestCase):
    """Tests tags for posts."""

    def setUp(self):
        self.tag = Tag(tag_name="TestTag")
        db.session.add(self.tag)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_view_tags(self):
        with app.test_client() as client:
            resp = client.get('/tags')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestTag', html)
    
    def test_new_tag_form(self):
        with app.test_client() as client:
            resp = client.get('/tags_new')

            self.assertEqual(resp.status_code, 200)

    def test_create_tag(self):
        with app.test_client() as client:
            resp = client.post('/tags_new', data={'tag_name': 'NewTestTag'}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            tag = Tag.query.filter_by(tag_name='NewTestTag').first()
            self.assertIsNotNone(tag)

    def test_show_tag_details(self):
        with app.test_client() as client:
            resp = client.get('/tags/1')
            self.assertEqual(resp.status_code, 200)

    def test_edit_tag_form(self):
        with app.test_client() as client:
            resp = client.get('tags/1/edit')
            self.assertEqual(resp.status_code, 200)

    def test_delete_tag(self):
        with app.test_client() as client:
            resp = client.post('tags/1/delete', follow_redirects=True)
            deleted_tag = Tag.query.get(1)
            self.assertIsNone(deleted_tag)
            self.assertEqual(resp.status_code, 200)