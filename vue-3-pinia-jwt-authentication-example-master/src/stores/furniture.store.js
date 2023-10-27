import { defineStore } from 'pinia';

import { fetchWrapper } from '@/helpers';

const baseUrl = `${import.meta.env.VITE_API_URL}`;


const createBonitaInstance = async () => {
    const responseListProcesses = await fetchWrapper.get(`${baseUrl}/bonita/list-processes/`)
    const processId = responseListProcesses[0].id
    const response = await fetchWrapper.post(`${baseUrl}/bonita/instantiate/${processId}/`)
    return response.caseId
}

export const useFurnitureStore = defineStore({
    id: 'furnitures',
    state: () => ({
        furnitures: {}
    }),
    actions: {
        async getAll() {
            this.furnitures = { loading: true }
            fetchWrapper.get(`${baseUrl}/muebles/`)
                .then(data => {
                    const furnitures = data.map(furniture => {
                        return {
                            id: furniture.id,
                            name: furniture.nombre,
                            description: furniture.descripcion,
                            finished: furniture.terminada
                        }
                    })
                    this.furnitures = furnitures
                    console.log(this.furnitures)
                })
                .catch(error => this.furnitures = { error })
        },
        async delete(id) {
            fetchWrapper.delete(`${baseUrl}/mueble/${id}/`).catch(error => this.furnitures = { error })
        },
        async create(values) {
            this.furnitures = { loading: true }
            const data = {
                nombre: values.name,
                descripcion: values.description
            }
            const response = await fetchWrapper.post(`${baseUrl}/mueble/`, data).catch(error => this.furnitures = { error })
            const caseId = await createBonitaInstance()
            const patchResponse = await fetchWrapper.patch(`${baseUrl}/mueble/${response.id}/`, { instancia_bonita: caseId }).catch(error => this.furnitures = { error })
        },
        async finish(id) {
            const patchResponse = await fetchWrapper.patch(`${baseUrl}/mueble/${id}/`, { terminada: true }).catch(error => this.furnitures = { error })
        },
    }
})
