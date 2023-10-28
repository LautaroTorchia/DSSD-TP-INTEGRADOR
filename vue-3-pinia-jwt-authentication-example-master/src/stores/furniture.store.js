import { defineStore } from 'pinia'

import { fetchWrapper } from '@/helpers'

const baseUrl = `${import.meta.env.VITE_API_URL}`

export const useFurnitureStore = defineStore({
    id: 'furnitures',
    state: () => ({
        furniture: {}
    }),
    actions: {
        async getAll() {
            const response = await fetchWrapper.get(`${baseUrl}/coleccion/muebles/`)
            return response
        },
        async getCollectionFurniture(collectionId) {
            const response = await fetchWrapper.get(`${baseUrl}/coleccion/muebles/`)
            const filteredFurniture = response.filter(furniture => furniture.collection_id === collectionId.toStrting())
            return filteredFurniture
        },
        async deleteFurniture(id) {
            await fetchWrapper.delete(`${baseUrl}/coleccion/muebles/${id}/`)
        },
        async updateFurniture(id, furniture) {
            await fetchWrapper.patch(`${baseUrl}/coleccion/muebles/${id}/`, furniture)
        },
        async createFurniture(furniture) {
            const response = await fetchWrapper.post(`${baseUrl}/coleccion/muebles/`, furniture)
            return response
        }
    }
})
