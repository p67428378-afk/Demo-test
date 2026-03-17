import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function LoanOfficerDashboard() {
  const [applications, setApplications] = useState([]);
  const [message, setMessage] = useState('');

  const fetchApplications = async () => {
    try {
      // For now, let's assume a token is available for loan_officer_id 1
      // In a real app, this would come from a login process
      const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJsb2Fub2ZmaWNlckBleGFtcGxlLmNvbSIsInJvbGUiOiJMb2FuIE9mZmljZXIiLCJleHAiOjE3NDIyOTQ0MDB9.some_dummy_token_for_officer"; // Replace with actual token

      const response = await axios.get(`${API_URL}/loan-applications/pending/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setApplications(response.data);
    } catch (error) {
      setMessage(`Error fetching applications: ${error.response?.data?.detail || error.message}`);
      console.error('Error fetching applications:', error.response?.data || error.message);
    }
  };

  useEffect(() => {
    fetchApplications();
  }, []);

  const handleReview = async (applicationId, decision) => {
    try {
      const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJsb2Fub2ZmaWNlckBleGFtcGxlLmNvbSIsInJvbGUiOiJMb2FuIE9mZmljZXIiLCJleHAiOjE3NDIyOTQ0MDB9.some_dummy_token_for_officer"; // Replace with actual token

      await axios.put(`${API_URL}/loan-applications/${applicationId}/review`, {
        status: decision,
        comments: `Application ${decision.toLowerCase()} by loan officer.`
      }, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setMessage(`Application ${applicationId} ${decision.toLowerCase()} successfully.`);
      fetchApplications(); // Refresh the list
    } catch (error) {
      setMessage(`Error reviewing application: ${error.response?.data?.detail || error.message}`);
      console.error('Error reviewing application:', error.response?.data || error.message);
    }
  };

  return (
    <div>
      <h2>Loan Officer Dashboard</h2>
      {message && <p>{message}</p>}
      {applications.length === 0 ? (
        <p>No pending applications.</p>
      ) : (
        <ul>
          {applications.map((app) => (
            <li key={app.id}>
              <h3>Application ID: {app.id}</h3>
              <p>Applicant ID: {app.applicant_id}</p>
              <p>Loan Amount: ${app.loan_amount}</p>
              <p>Tenure: {app.loan_tenure} months</p>
              <p>Status: {app.status}</p>
              <button onClick={() => handleReview(app.id, 'Approved')}>Approve</button>
              <button onClick={() => handleReview(app.id, 'Rejected')}>Reject</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default LoanOfficerDashboard;
