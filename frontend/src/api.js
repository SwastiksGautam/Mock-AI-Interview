import axios from 'axios';

// Create a reusable Axios instance configured for your backend
const apiClient = axios.create({
  baseURL: 'https://mock-ai-interview-sb08.onrender.com/api',
  headers: { 'Content-Type': 'application/json' },
});

/**
 * Starts a new interview session.
 * @returns {Promise<Object>} The initial interview data, including session_id and the first question.
 */
export const startInterview = async () => {
  try {
    const response = await apiClient.post('/start');
    return response.data;
  } catch (error) {
    console.error("API Error: Failed to start interview", error);
    throw error; // Re-throw the error to be caught by the component
  }
};

/**
 * Submits a candidate's answer to the backend.
 * @param {string} sessionId - The ID of the current interview session.
 * @param {string} answer - The candidate's answer text.
 * @returns {Promise<Object>} The response, containing either the next question or the final summary.
 */
export const submitAnswer = async (sessionId, answer) => {
  try {
    const response = await apiClient.post('/answer', { session_id: sessionId, answer });
    return response.data;
  } catch (error) {
    console.error("API Error: Failed to submit answer", error);
    throw error;
  }
};