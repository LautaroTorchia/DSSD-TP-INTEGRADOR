


export const instantiateBonita = async (id,ticketData) => {
  const api = axios.create({
    baseURL: `${process.env.API_URL}`,
    headers: {
        Authorization: `Bearer ${data.accessToken}`, 
        'Content-Type': 'application/json',
    },
})

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