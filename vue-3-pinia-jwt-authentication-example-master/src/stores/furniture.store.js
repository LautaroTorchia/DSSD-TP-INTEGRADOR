import { defineStore } from 'pinia'

import { fetchWrapper } from '@/helpers'

const baseUrl = `${import.meta.env.VITE_API_URL}`

export const useFurnitureStore = defineStore({
    id: 'furniture',
    state: () => ({
        furniture: {}
    }),
    actions: {
        async getCollectionFurniture(collectionId) {
            const response = await fetchWrapper.get(`${baseUrl}/coleccion/muebles/`)
            const filteredFurniture = response.filter(furniture => furniture.collection_id == collectionId)
            this.furniture = filteredFurniture
            return filteredFurniture
        },
        async getById(id) {
            return this.furniture.find(furniture => furniture.id == id)
        },
        async delete(id) {
            try {
                await fetchWrapper.delete(`${baseUrl}/coleccion/muebles/${id}/`);
                this.furniture = this.furniture.filter(furniture => furniture.id !== id);
            } catch (error) {
                this.furniture = { error };
            }
        },
        async update(id, furniture) {
            await fetchWrapper.patch(`${baseUrl}/coleccion/muebles/${id}/`, furniture)
        },
        async create(furniture) {
            const furnitureRequest = {
                nombre: furniture.name,
                plazo_fabricacion: furniture.estimated_days,
                fecha_lanzamiento_estimada: furniture.estimated_release,
                descripcion: furniture.description,
                imagen: furniture.image,
                plan_fabricacion: furniture.manufacturing_plan,
                materiales: furniture.materials,
                coleccion: furniture.collection_id
            }
            const response = await fetchWrapper.post(`${baseUrl}/coleccion/muebles/`, furnitureRequest)
            return response
        }
    }
})
