import createApiClient from "@/axios/axios";

export const loginToBonita = async (username, password, token) => {
  const api = createApiClient(); // Create an Axios instance with the provided token
  try {
    const response = await api.post('/bonita/login/', {
      username,
      password,
    });

    if (response.status === 204) {
      return { success: true };
    } else {
      throw new Error(`Error: ${response.statusText}`);
    }
  } catch (error) {
    throw new Error(`Error: ${error.message}`);
  }
};
