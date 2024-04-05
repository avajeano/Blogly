from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bogly_test'

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

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
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "TestFirstName2", "last_name": "TestLastName2", "image_url":"https://img.freepik.com/free-vector/user-blue-gradient_78370-4692.jpg?w=826&t=st=1712240115~exp=1712240715~hmac=ec275943900481bfc64f790c547f043f8554bf3398e6cf2fab36de9dc3f590ce"}
            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
    
    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete")
            deleted_user = User.query.get(self.user_id)

            self.assertIsNone(deleted_user)