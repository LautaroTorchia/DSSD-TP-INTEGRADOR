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
        async getAll() {
            this.collections = { loading: true }
            fetchWrapper.get(`${baseUrl}/coleccion/`)
                .then(data => {
                    const collections = data.map(collection => {
                        return {
                            id: collection.id,
                            name: collection.nombre,
                            description: collection.descripcion,
                            caseId: collection.instancia_bonita,
                            finished: collection.terminada
                        }
                    })
                    this.collections = collections
                    console.log(this.collections)
                })
                .catch(error => this.collections = { error })
        },
        async delete(id) {
            fetchWrapper.delete(`${baseUrl}/coleccion/${id}/`).catch(error => this.collections = { error })
        },
        async create(values) {
            this.collections = { loading: true }
            const data = {
                nombre: values.name,
                descripcion: values.description
            }
            const response = await fetchWrapper.post(`${baseUrl}/coleccion/`, data).catch(error => this.collections = { error })
            const caseId = await createBonitaInstance()
            const patchResponse = await fetchWrapper.patch(`${baseUrl}/coleccion/${response.id}/`, { instancia_bonita: caseId }).catch(error => this.collections = { error })
        },
        async finish(collection) {
            
            const patchResponse = await fetchWrapper.patch(`${baseUrl}/coleccion/${collection.id}/`, { terminada: true }).catch(error => this.collections = { error })
        },
    }
})
