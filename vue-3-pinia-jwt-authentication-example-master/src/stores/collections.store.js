import { defineStore } from 'pinia';

import { fetchWrapper } from '@/helpers';

const baseUrl = `${import.meta.env.VITE_API_URL}`;


const createBonitaInstance = async () => {
    const responseListProcesses = await fetchWrapper.get(`${baseUrl}/bonita/list-processes/`)
    const processId = responseListProcesses[0].id
    const response = await fetchWrapper.post(`${baseUrl}/bonita/instantiate/${processId}/`)
    return response.caseId
}

export const useCollectionsStore = defineStore({
    id: 'collections',
    state: () => ({
        collections: {}
    }),
    actions: {
        async delete(id) {
            this.collections = { loading: true }
            fetchWrapper.delete(`${baseUrl}/coleccion/${id}/`).catch(error => this.collections = { error })
        },
        async create(values) {
            this.collections = { loading: true }
            const data ={
                nombre: values.name,
                descripcion: values.description
            }
            const response = await fetchWrapper.post(`${baseUrl}/coleccion/`, data).catch(error => this.collections = { error })
            const caseId = await createBonitaInstance()
            const patchResponse = await fetchWrapper.patch(`${baseUrl}/coleccion/${response.id}/`, { instancia_bonita: caseId }).catch(error => this.collections = { error })
        },
        async getAll() {
            this.collections = { loading: true }
            fetchWrapper.get(`${baseUrl}/coleccion/`)
                .then(data => {
                    console.log(data)
                    const collections = data.map(collection => {
                        return {
                            id: collection.id,
                            name: collection.nombre,
                            description: collection.descripcion
                        }
                    })
                    console.log(collections)
                    this.collections = collections
                })
                .catch(error => this.collections = { error })
        }
    }
})
