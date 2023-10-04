import { API_URL } from '@/../config';

export const listBonitaProcesses = async () => {
  try {
    const response = await fetch(`${API_URL}bonita/list-processes/`, {
      method: 'GET',
      headers: {
        'accept': 'application/json',
      },
    });

    if (response.ok) {
      // Return the response data or handle as needed
      return response.json();
    } else {
      throw new Error(`Error: ${response.statusText}`);
    }
  } catch (error) {
    throw new Error(`Error: ${error.message}`);
  }
};