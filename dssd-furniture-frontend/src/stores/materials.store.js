import { defineStore } from 'pinia'
import { fetchWrapper } from '@/helpers'

const baseUrl = `${import.meta.env.VITE_API_URL}`

export const useMaterialsStore = defineStore({
    id: 'materials',
    state: () => ({
        materials: [],
    }),
    actions: {
        async getAll() {
            try {
                const response = await fetchWrapper.get(`${baseUrl}/proveedores/materiales/`)
                this.materials = response
                return response
            } catch (error) {
                console.error(error)
            }
        },
        async create(material) {
            try {
                const response = await fetchWrapper.post(`${baseUrl}/proveedores/materiales/`, material)
                this.materials.push(response)
            } catch (error) {
                console.error(error)
            }
        },
    },
})
