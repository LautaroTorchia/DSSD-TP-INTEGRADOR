import createApiClient from "@/axios/axios";

export const editCollection = async (id,collectionData) => {
    const api = createApiClient();
    try {
        const response = await api.patch(`coleccion/${id}/`, collectionData);
        if (response.status === 200) {
            return response.data;
        } else {
            throw new Error(`Error: ${response.statusText}`);
        }
    } catch (error) {
        console.error('Edit Collection Error:', error);
    }
};