import unittest
import json
from app import app, receipts


class ReceiptProcessorTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client for Flask app."""
        self.app = app.test_client()
        self.app.testing = True

    def test_process_receipt_valid(self):
        """Test processing a valid receipt."""
        receipt_data = {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "15:01",
            "items": [
                {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                {"shortDescription": "Emils Cheese Pizza", "price": "12.25"}
            ],
            "total": "35.35"
        }
        response = self.app.post(
            "/receipts/process",
            data=json.dumps(receipt_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn("id", response_data)
        self.assertTrue(response_data["id"] in receipts)  # Check if the ID is stored

    def test_process_receipt_invalid(self):
        """Test processing an invalid receipt."""
        invalid_data = {"retailer": "Target"}  # Wrong format, missing data
        response = self.app.post(
            "/receipts/process",
            data=json.dumps(invalid_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn("error", response_data)

    def test_get_points_valid(self):
        """Test retrieving points for a valid receipt ID."""
        # First, process a receipt
        receipt_data = {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "15:01",
            "items": [
                {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                {"shortDescription": "Emils Cheese Pizza", "price": "12.25"}
            ],
            "total": "35.35"
        }
        process_response = self.app.post(
            "/receipts/process",
            data=json.dumps(receipt_data),
            content_type="application/json",
        )
        receipt_id = json.loads(process_response.data)["id"]

        # Retrieve points
        points_response = self.app.get(f"/receipts/{receipt_id}/points")
        self.assertEqual(points_response.status_code, 200)
        points_data = json.loads(points_response.data)
        self.assertIn("points", points_data)
        self.assertIsInstance(points_data["points"], int)

    def test_get_points_invalid_id(self):
        """Test retrieving points for a non-existent receipt ID."""
        response = self.app.get("/receipts/nonexistent-id/points")
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.data)
        self.assertIn("error", response_data)

if __name__ == "__main__":
    unittest.main()
