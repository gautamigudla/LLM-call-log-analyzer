from flask import request, jsonify
from app import app
import uuid
import json
import requests
from datetime import datetime, timedelta
import re
from app.model_handler import answer_question
from threading import Thread

DATA_STORE_PATH = 'data_store.json'

data_store = {
    "questions": {},
    "facts": {},
    "document_dates": [],
    "processing_status": {}
}

def save_data():
    with open(DATA_STORE_PATH, 'w') as f:
        json.dump(data_store, f, indent=4, default=str)

def load_data():
    global data_store
    try:
        with open(DATA_STORE_PATH) as f:
            data_store = json.load(f)
            # Ensuring all date strings are converted back to date objects
            data_store["document_dates"] = [datetime.fromisoformat(date).date() for date in data_store["document_dates"]]
            # Initializing processing status if not present
            if "processing_status" not in data_store:
                data_store["processing_status"] = {}
    except FileNotFoundError:
        pass  # Keep initial structure if file not found

def extract_date_from_url(url):
    match = re.search(r'(\d{4})(\d{2})(\d{2})', url)
    if match:
        year, month, day = map(int, match.groups())
        return datetime(year, month, day).date()
    return None

def process_documents(question_id, question, document_urls, auto_approve):
    responses = []
    document_dates = []
    for doc_url in document_urls:
        try:
            response = requests.get(doc_url)
            response.raise_for_status()
            document_text = response.text

            date = extract_date_from_url(doc_url)
            if date:
                document_dates.append(date)
                fact_id = str(uuid.uuid4())
                answer = answer_question(question, document_text)
                if answer:
                    approved_status = True if auto_approve else None
                    responses.append({"fact_id": fact_id, "date": date.isoformat(), "fact": answer, "timestamp": datetime.now().isoformat(), "approved": approved_status})
        except requests.RequestException as e:
            print(f"Error downloading {doc_url}: {e}")

    if document_dates:
        data_store["document_dates"].extend(document_dates)
        data_store["document_dates"] = list(set(data_store["document_dates"]))  # Remove duplicates and sort
        data_store["document_dates"].sort()

    data_store["questions"][question_id] = {"question": question, "documents": document_urls}
    data_store["facts"][question_id] = responses
    data_store["processing_status"][question_id] = "done"  # Update processing status
    save_data()

@app.route('/submit_question_and_documents', methods=['POST'])
def submit_question_and_documents():
    data = request.json
    question = data.get("question")
    document_urls = data.get("documents", [])
    auto_approve = data.get("autoApprove", False)
    
    question_id = str(uuid.uuid4())
    data_store["processing_status"][question_id] = "processing"  # Mark as processing
    save_data()
    
    # Process documents in a separate thread to not block the request
    Thread(target=process_documents, args=(question_id, question, document_urls, auto_approve)).start()
    
    return jsonify({"status": "success", "question_id": question_id}), 200

@app.route('/get_question_and_facts', methods=['GET'])
def get_question_and_facts():
    question_id = request.args.get("question_id")
    
    if question_id not in data_store["facts"]:
        return jsonify({"error": "Question ID not found"}), 404

    # Check processing status
    status = data_store["processing_status"].get(question_id, "processing")
    if status == "processing":
        return jsonify({"question": "What are our product design decisions?", "status": "processing"})

    # Respond with facts if processing is done
    question_details = data_store["questions"][question_id]
    facts_by_day = {}
    for fact in data_store["facts"][question_id]:
        date = fact["date"]
        if date not in facts_by_day:
            facts_by_day[date] = []
        fact_text = f"{fact['fact']} (approved: {fact['approved']})"
        facts_by_day[date].append(fact_text)

    return jsonify({
        "question": question_details["question"],
        "factsByDay": facts_by_day,
        "status": "done"
    }), 200

@app.route('/approve_fact', methods=['POST'])
def approve_fact():
    data = request.json
    question_id = data.get("question_id")
    fact_id = data.get("fact_id")
    approval_status = data.get("approval_status", False)

    # Update the fact's approval status
    for fact in data_store["facts"].get(question_id, []):
        if fact["fact_id"] == fact_id:
            fact["approved"] = approval_status
            save_data()
            return jsonify({"status": "success", "message": "Fact approval status updated"}), 200

    return jsonify({"error": "Fact or question not found"}), 404

if __name__ == "__main__":
    load_data()
    app.run(debug=True)
