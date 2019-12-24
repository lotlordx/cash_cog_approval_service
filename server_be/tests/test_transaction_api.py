
import unittest
import json
from app import db, create_app


class TransactionListTestCase(unittest.TestCase):
    """This class represents the transaction test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config='testing')
        self.client = self.app.test_client
        self.transaction_list = json.dumps({"amount": 639,
                                            "description": "Hic quae illum quas sed quisquam quos.",
                                            "uuid": "763a9cfd-b7d9-4ef0-eru3-f9d9f46c91b0",
                                            "currency": "MWK",
                                            "created_at": "2019-12-04T01:04:14",
                                            "employee": {
                                                "first_name": "Britt",
                                                "last_name": "Rogner",
                                                "uuid": "b122689a-755e-43bf-b490-8e54de9d3b86"
                                            }
                                            })
        self.transaction_list_updated = json.dumps({
            "amount": 20000,
            "description": "i would like to travel to the east",
            "approval_status": "approved",
            "currency": 1
        })

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_transaction_creation(self):
        """Test API can create a transaction (POST request)"""

        res = self.client().post('/api/v1/transactions', data=self.transaction_list, content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn('763a9cfd-b7d9-4ef0-eru3-f9d9f46c91b0', str(res.data))

    def test_api_can_get_all_transactions(self):
        """Test API can get a transaction (GET request)."""
        self.test_transaction_creation()
        res = self.client().get('/api/v1/transactions')
        self.assertEqual(res.status_code, 200)
        self.assertIn('763a9cfd-b7d9-4ef0-eru3-f9d9f46c91b0', str(res.data))

    def test_transaction_can_be_updated(self):
        """Test API can edit an existing transaction. (PUT request)"""
        self.test_transaction_creation()
        res = self.client().put('api/v1/transactions/763a9cfd-b7d9-4ef0-eru3-f9d9f46c91b0',
                                data=self.transaction_list_updated, content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertIn("i would like to travel to the east", str(res.data))

    def test_transaction_deletion(self):
        """Test API can delete an existing transaction. (DELETE request)."""
        self.test_transaction_creation()
        res = self.client().delete(
            '/transactions/763a9cfd-b7d9-4ef0-eru3-f9d9f46c91b0')
        self.assertEqual(res.status_code, 200)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
