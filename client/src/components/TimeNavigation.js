import React, { useState } from 'react';

const TimeNavigation = ({ onDateChange }) => {
  const [date, setDate] = useState('');

  return (
    <div>
      <input
        type="date"
        value={date}
        onChange={(e) => {
          setDate(e.target.value);
          onDateChange(e.target.value);
        }}
      />
    </div>
  );
};

export default TimeNavigation;