// QAScreen.js
import React from 'react';
import FactsDisplay from './FactsDisplay';
import TimeNavigation from './TimeNavigation';

const QAScreen = ({ questionId }) => {
  return (
    <>
      <FactsDisplay questionId={questionId} />
      <TimeNavigation onDateChange={(date) => console.log('Date changed to:', date)} />
    </>
  );
};

export default QAScreen;