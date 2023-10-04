import createApiClient from "@/axios/axios";


export const instantiateBonita = async (id,ticketData) => {
  const api = createApiClient();

  try {
    const response = await api.post(`/bonita/instantiate/${id}/`, ticketData, {
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