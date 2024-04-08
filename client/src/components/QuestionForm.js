import React, { useState } from 'react';

const QuestionForm = ({ onQuestionSubmit }) => {
  const [question, setQuestion] = useState('');
  const [documents, setDocuments] = useState(['']);

  const handleAddDocument = () => {
    setDocuments([...documents, '']);
  };

  const handleDocumentChange = (index, value) => {
    const newDocuments = documents.map((doc, i) => (
      i === index ? value : doc
    ));
    setDocuments(newDocuments);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    console.log('Question and documents submitted:', { question, documents });

    setTimeout(() => {
      const mockResponse = { question_id: 'mock_id' };

      // Check if onQuestionSubmit is a function before calling it
      if (typeof onQuestionSubmit === 'function') {
        onQuestionSubmit(mockResponse.question_id);
      } else {
        console.error('onQuestionSubmit is not a function');
      }

      // Uncomment the line below to simulate an error
      // console.error('Error submitting question and documents:', { message: 'Mock error' });
    }, 1000);
  };

  return (
    <form onSubmit={handleSubmit} className="question-form">
      <label htmlFor="questionInput">Enter your question:</label>
      <input
        id="questionInput"
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="What are our product design decisions?"
        required
      />
      <div className="document-urls">
        {documents.map((doc, index) => (
          <div key={index} className="document-url">
            <input
              type="text"
              value={doc}
              onChange={(e) => handleDocumentChange(index, e.target.value)}
              placeholder="Enter document URL"
              required={index === 0} // Only the first document is required
            />
          </div>
        ))}
      </div>
      <button type="button" onClick={handleAddDocument}>
        Add Another Document
      </button>
      <button type="submit">Submit Question</button>
    </form>
  );
};

export default QuestionForm;
