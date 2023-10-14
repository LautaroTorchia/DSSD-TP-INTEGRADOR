export const instantiateBonita = async (api,id,ticketData) => {
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