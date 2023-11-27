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
            const filteredFurniture = JSON.parse(localStorage.getItem('furniture')).furniture.filter(furniture => furniture.coleccion == collectionId) 
            this.furniture = filteredFurniture
            return filteredFurniture
        },
        async getAll() {
            try {
                this.furniture = { loading: true }
                const data = await fetchWrapper.get(`${baseUrl}/coleccion/muebles/`)
                const processedData = data.map(item => {
                    item.materiales = item.materiales.replace(/[\[\]']+/g,'').split(',')
                    return item
                })
                this.furniture = processedData
            } catch (error) {
                this.furniture = { error }
            }
        },
        async getFurnitureDetail(id) {
            const response = await fetchWrapper.get(`${baseUrl}/coleccion/muebles/${id}/`)
            response.materiales = response.materiales.replace(/[\[\]']+/g,'').split(',')
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

            const response = await sendFile.post(`${baseUrl}/coleccion/muebles/`, furniture)

            return response
        }
    }
})
