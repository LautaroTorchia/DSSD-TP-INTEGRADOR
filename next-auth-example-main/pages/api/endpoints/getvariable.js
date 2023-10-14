import createApiClient from "@/axios/axios";

export const updateBonitaCaseVariable = async (instance, variable, value) => {
  const api = createApiClient();
  try {
    const response = await api.put(`bonita/update-case-variable/${instance}/${variable}/`, value);

    if (response.status === 200) {
      return response.data;
    } else {
      throw new Error(`Error: ${response.statusText}`);
    }
  } catch (error) {
    throw new Error(`Error: ${error.message}`);
  }
};
