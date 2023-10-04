import createApiClient from "@/axios/axios";


export const listBonitaProcesses = async () => {
  const api = createApiClient();
  try {
    const response = await api.get('bonita/list-processes/');

    if (response.status === 200) {
      // Return the response data or handle as needed
      return response.data;
    } else {
      throw new Error(`Error: ${response.statusText}`);
    }
  } catch (error) {
    throw new Error(`Error: ${error.message}`);
  }
};