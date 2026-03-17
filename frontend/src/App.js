import React, { useState } from 'react';
import LoanApplicationForm from './components/LoanApplicationForm';
import LoanOfficerDashboard from './components/LoanOfficerDashboard';

function App() {
  const [userType, setUserType] = useState(null); // 'applicant' or 'officer'

  const renderContent = () => {
    if (userType === 'applicant') {
      return <LoanApplicationForm />;
    } else if (userType === 'officer') {
      return <LoanOfficerDashboard />;
    } else {
      return (
        <div>
          <h1>Welcome to the Online Loan Application Platform</h1>
          <button onClick={() => setUserType('applicant')}>I am a Loan Applicant</button>
          <button onClick={() => setUserType('officer')}>I am a Loan Officer</button>
        </div>
      );
    }
  };

  return (
    <div className="App">
      {renderContent()}
    </div>
  );
}

export default App;
