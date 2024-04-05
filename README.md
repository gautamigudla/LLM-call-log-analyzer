Call Log Analyzer Web Application
This web application processes and extracts information from a set of call logs using a Language Model (LLM). It allows users to set a single question and provide a list of call logs, from which a set of facts/answers are extracted. Users can also navigate through time to view the state of knowledge at different points based on the processed documents.
Features
•	Process call logs to extract relevant information based on a user-provided question.
•	Display extracted facts/answers in a question and answer screen.
•	Allow users to navigate through time to view historical data.
•	Provide a document addition screen to add new call transcripts.
•	Highlight facts added or removed in the last 24 hours.
•	Handle contradictions within and across documents, suggesting necessary modifications.

Technologies Used
•	Frontend: HTML, CSS, JavaScript
•	Backend: Python
•	Language Model (LLM):Text-to-Text Transfer Transformer(T5), Google Colab
•	Frameworks: Frontend - React.js,Backend - Flask
•	Additional Tools: AWS (for hosting)
