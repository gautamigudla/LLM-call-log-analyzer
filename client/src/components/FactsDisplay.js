import React, { useState, useEffect } from 'react';
import axios from 'axios';

const FactsDisplay = ({ questionId }) => {
  const [facts, setFacts] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Function to check if the fact's date is within the last 24 hours
  const isRecent = (factDate) => {
    const now = new Date();
    const factDateObj = new Date(factDate);
    const oneDay = 24 * 60 * 60 * 1000; // hours*minutes*seconds*milliseconds
    return now - factDateObj < oneDay;
  };

  useEffect(() => {
    const fetchFacts = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await axios.get('/get_question_and_facts', { params: { question_id: questionId } });
        setFacts(response.data);
      } catch (error) {
        console.error('Error fetching facts:', error);
        setError('Failed to fetch facts');
      } finally {
        setIsLoading(false);
      }
    };

    if (questionId) {
      fetchFacts();
    }
  }, [questionId]);

  // Display a loading indicator when facts are being fetched
  if (isLoading) {
    return <div>Loading facts...</div>;
  }

  // Display an error message if there was an error fetching facts
  if (error) {
    return <div>{error}</div>;
  }

  // Display a message if there are no facts to display
  if (!facts || Object.keys(facts.factsByDay).length === 0) {
    return <div>No facts available.</div>;
  }

  // Display the facts if they are available
  return (
    <div>
      {Object.entries(facts.factsByDay).map(([date, factsList]) => (
        <div key={date}>
          <h3>{date}</h3>
          <ul>
            {factsList.map((fact, index) => (
              // Apply a different className if the fact is recent
              <li key={index} className={isRecent(date) ? 'recent-fact' : ''}>
                {fact}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
};

export default FactsDisplay;