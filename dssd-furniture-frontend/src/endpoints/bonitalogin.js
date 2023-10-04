import createApiClient from "@/axios/axios";

export const loginToBonita = async (username, password) => {
  const api = createApiClient();
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
