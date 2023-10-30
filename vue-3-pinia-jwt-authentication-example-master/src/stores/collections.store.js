import { defineStore } from 'pinia'
import { useFurnitureStore} from './furniture.store'
import { fetchWrapper } from '@/helpers'

const baseUrl = `${import.meta.env.VITE_API_URL}`


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
    getters: {
        getCollection: (state) => (id) => {
            return state.collections.find(collection => collection.id === id)
        }
    },
    actions: {
        async getAll() {
            try {
                this.collections = { loading: true }
                const data = await fetchWrapper.get(`${baseUrl}/coleccion/`)
                const furnitureStore = useFurnitureStore()

                const collections = await Promise.all(data.map(async collection => {
                    const furniture = await furnitureStore.getCollectionFurniture(collection.id)
                    return {
                        id: collection.id,
                        name: collection.nombre,
                        description: collection.descripcion,
                        caseId: collection.instancia_bonita,
                        finished: collection.terminada,
                        furniture: furniture,
                    }
                }))
                this.collections = collections
            } catch (error) {
                this.collections = { error }
            }
        },
        getById(id) {
            return this.collections.find(collection => collection.id == id)
        },
        async delete(id) {
            try {
                await fetchWrapper.delete(`${baseUrl}/coleccion/${id}/`);
                this.collections.splice(this.collections.findIndex(collection => collection.id === id), 1);
            } catch (error) {
                this.collections = { error };
            }
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
            try {
                const tasks = await fetchWrapper.get(`${baseUrl}/bonita/user-tasks/`)
                const task = tasks.find(task => task.rootCaseId === collection.caseId.toString())
                await fetchWrapper.post(`${baseUrl}/bonita/execute-user-task/${task.id}/`)
                await fetchWrapper.patch(`${baseUrl}/coleccion/${collection.id}/`, { terminada: true })
            } catch (error) {
                this.collections = { error }
            }
        },
        async update(collection) {
            const data = {
                nombre: collection.name,
                descripcion: collection.description
            }
            fetchWrapper.patch(`${baseUrl}/coleccion/${collection.id}/`, data).catch(error => this.collections = { error })
            localStorage.removeItem(collection.id)
        },
    }
})
