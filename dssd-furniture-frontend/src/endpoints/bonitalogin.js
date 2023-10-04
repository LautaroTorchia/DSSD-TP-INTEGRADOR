import { API_URL } from '@/../config';

export const loginToBonita = async (username, password) => {
  try {
    const response = await fetch(`${API_URL}bonita/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
      // Return the response data or handle as needed
      return { success: true };
    } else {
      throw new Error(`Error: ${response.statusText}`);
    }
  } catch (error) {
    throw new Error(`Error: ${error.message}`);
  }
};
