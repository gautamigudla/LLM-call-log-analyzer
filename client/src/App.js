import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import QAScreen from './components/QAScreen';
import DocAddScreen from './components/DocAddScreen';

function App() {
  const [questionId, setQuestionId] = useState(null);

  // Mock function for handling question submission
  const handleQuestionSubmit = (id) => {
    // Here you can handle what happens after a question is submitted
    // For now, we just set the questionId state
    setQuestionId(id);
    // You might also route the user to a different screen or show a confirmation message
  };

  return (
    <div className="App">
      <BrowserRouter>
        <nav>
          <Link to="/">Home</Link> | <Link to="/add-document">Add Document</Link>
        </nav>

        <Routes>
          {/* Pass the handleQuestionSubmit function to QAScreen */}
          <Route path="/" element={<QAScreen onQuestionSubmit={handleQuestionSubmit} questionId={questionId} />} />
          {/* Pass the handleQuestionSubmit function to DocAddScreen */}
          <Route path="/add-document" element={<DocAddScreen onQuestionSubmit={handleQuestionSubmit} />} />
          {/* Add other routes as needed */}
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
