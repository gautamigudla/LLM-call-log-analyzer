import json
import time
from flask_testing import TestCase
from app import app  # Make sure the app is imported correctly
from unittest.mock import patch
# Ensure the following import works as intended; adjust if necessary
from app.routes import data_store  

class FlaskTestCase(TestCase):

    def create_app(self):
        # Configuring the Flask app for testing
        app.config['TESTING'] = True
        return app

    def setUp(self):
        # Directly manipulating data_store before each test
        data_store.clear()
        data_store.update({
            "questions": {}, 
            "facts": {}, 
            "document_dates": [], 
            "processing_status": {}
        })

    def tearDown(self):
        # Optional: Additional cleanup after tests, if required
        pass

    @patch('app.routes.requests.get')
    def test_submit_question_and_documents(self, mock_get):
        # Mocking the external call to requests.get
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "Example document text."
        
        # Testing document submission
        response = self.client.post('/submit_question_and_documents', 
                                    data=json.dumps({
                                        "question": "What color should we use?",
                                        "documents": ["https://example.com/call_log_20240317_104111.txt"],
                                        "autoApprove": True
                                    }), 
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("question_id", response.json)
        
        # Simulating processing delay
        time.sleep(1)  
        question_id = response.json["question_id"]

        # Verifying processing status
        self.assertIn(question_id, data_store["processing_status"])
        self.assertEqual(data_store["processing_status"][question_id], "done")

    def test_get_question_and_facts_processing(self):
        # Setup for testing retrieval of processing facts
        mock_question_id = "test-question-id"
        data_store["questions"][mock_question_id] = {"question": "Mock question", "documents": []}
        data_store["facts"][mock_question_id] = []
        data_store["processing_status"][mock_question_id] = "processing"

        # Making a GET request to retrieve facts
        response = self.client.get(f'/get_question_and_facts?question_id={mock_question_id}')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.json)
        self.assertEqual(response.json["status"], "processing")

if __name__ == '__main__':
    import unittest
    unittest.main()
