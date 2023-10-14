


export const listBonitaProcesses = async () => {
  const api = axios.create({
    baseURL: `${process.env.API_URL}`,
    headers: {
        Authorization: `Bearer ${data.accessToken}`, 
        'Content-Type': 'application/json',
    },
})
  try {
    const response = await api.get('bonita/list-processes/');

    if (response.status === 200) {
      return response.data;
    } else {
      throw new Error(`Error: ${response.statusText}`);
    }
  } catch (error) {
    throw new Error(`Error: ${error.message}`);
  }
};