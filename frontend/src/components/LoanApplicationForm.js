import React, { useState } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function LoanApplicationForm() {
  const [formData, setFormData] = useState({
    applicant_id: 1, // Placeholder, will be dynamic with auth
    loan_amount: '',
    loan_tenure: '',
    financial_details: '',
    bank_name: '',
    account_number: '',
    ifsc_swift_code: '',
    legal_consent: false,
  });
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // For now, let's assume a token is available for applicant_id 1
      // In a real app, this would come from a login process
      const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhcHBsaWNhbnQxQGV4YW1wbGUuY29tIiwicm9sZSI6IkFwcGxpY2FudCIsImV4cCI6MTc0MjI5NDQwMH0.some_dummy_token"; // Replace with actual token

      const response = await axios.post(`${API_URL}/loan-applications/`, formData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setMessage('Application submitted successfully!');
      console.log(response.data);
    } catch (error) {
      setMessage(`Error submitting application: ${error.response?.data?.detail || error.message}`);
      console.error('Error submitting application:', error.response?.data || error.message);
    }
  };

  return (
    <div>
      <h2>Loan Application Form</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Applicant ID:</label>
          <input
            type="number"
            name="applicant_id"
            value={formData.applicant_id}
            onChange={handleChange}
            required
            disabled // Will be set by auth later
          />
        </div>
        <div>
          <label>Loan Amount:</label>
          <input
            type="number"
            name="loan_amount"
            value={formData.loan_amount}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Loan Tenure (months):</label>
          <input
            type="number"
            name="loan_tenure"
            value={formData.loan_tenure}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Financial Details:</label>
          <textarea
            name="financial_details"
            value={formData.financial_details}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Bank Name:</label>
          <input
            type="text"
            name="bank_name"
            value={formData.bank_name}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Account Number:</label>
          <input
            type="text"
            name="account_number"
            value={formData.account_number}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>IFSC/SWIFT Code:</label>
          <input
            type="text"
            name="ifsc_swift_code"
            value={formData.ifsc_swift_code}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>
            <input
              type="checkbox"
              name="legal_consent"
              checked={formData.legal_consent}
              onChange={handleChange}
              required
            />
            I agree to the terms and conditions.
          </label>
        </div>
        <button type="submit">Submit Application</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default LoanApplicationForm;
