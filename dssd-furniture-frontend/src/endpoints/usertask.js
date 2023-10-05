import createApiClient from "@/axios/axios";

export const listBonitaUserTask = async () => {
  const api = createApiClient();
  try {
    const response = await api.get('bonita/user-tasks/');

    if (response.status === 200) {
      return response.data;
    } else {
      throw new Error(`Error: ${response.statusText}`);
    }
  } catch (error) {
    throw new Error(`Error: ${error.message}`);
  }
};

export const executeBonitaTask = async (id,comment) => {
    const api = createApiClient();
  
    try {
      const response = await api.post(`/bonita/execute-user-task/${id}/`, comment, {
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json'
        },
      });
      return response; 
    } catch (error) {
      throw new Error(`Error: ${error.message}`);
    }
  };