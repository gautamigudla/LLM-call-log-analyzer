// In DocAddScreen.js
import React from 'react';
import QuestionForm from './QuestionForm';

const DocAddScreen = () => {
  const handleQuestionSubmit = (questionId) => {
    console.log(`Submitted question ID: ${questionId}`);
    // Implement what you want to do with the question ID
  };

  return (
    <div>
      <h2>Add Document</h2>
      <QuestionForm onQuestionSubmit={handleQuestionSubmit} />
    </div>
  );
};

export default DocAddScreen;
