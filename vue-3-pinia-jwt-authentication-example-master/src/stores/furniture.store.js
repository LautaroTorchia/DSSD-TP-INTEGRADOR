import { defineStore } from 'pinia'

import { fetchWrapper, sendFile } from '@/helpers'

const baseUrl = `${import.meta.env.VITE_API_URL}`


export const useFurnitureStore = defineStore({
    id: 'furniture',
    state: () => (
        {furniture: {}
    }),
    persist: true,//https://prazdevs.github.io/pinia-plugin-persistedstate/guide/config.html
    getters: {
        getCollections: (state) => {
            return state.furniture
        }
    },
    actions: {
        async getCollectionFurniture(collectionId) {
            await this.getAll()  
            const filteredFurniture = this.furniture.filter(furniture => furniture.coleccion == collectionId)
            this.furniture = filteredFurniture
            return filteredFurniture
        },
        async getAll() {
            try {
                this.furniture = { loading: true }
                const data = await fetchWrapper.get(`${baseUrl}/coleccion/muebles/`)
                this.furniture = data
            } catch (error) {
                this.furniture = { error }
            }
        },
        async getFurnitureDetail(id) {
            const response = await fetchWrapper.get(`${baseUrl}/coleccion/muebles/${id}/`)
            return response
        },

        async getById(id) {
            return this.furniture.find(furniture => furniture.id == id)
        },
        async delete(id) {
            try {
                await fetchWrapper.delete(`${baseUrl}/coleccion/muebles/${id}/`)
                this.furniture = this.furniture.filter(furniture => furniture.id !== id)
            } catch (error) {
                this.furniture = { error }
            }
        },
        async update(id, furniture) {
            await fetchWrapper.patch(`${baseUrl}/coleccion/muebles/${id}/`, furniture)
        },
        async create(furniture) {

            console.log(furniture)

            throw new Error('Not implemented')
            const response = await sendFile.post(`${baseUrl}/coleccion/muebles/`, furniture)
            return response
        }
    }
})
