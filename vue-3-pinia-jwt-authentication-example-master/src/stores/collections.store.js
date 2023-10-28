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
    actions: {
        async getAll() {
            try {
                this.collections = { loading: true }
                const data = await fetchWrapper.get(`${baseUrl}/coleccion/`)
                const furnitureStore = useFurnitureStore()
                const furnitureData = await furnitureStore.getAll()

                const collections = data.map(collection => {
                    const furniture = furnitureData.filter(furniture => furniture.coleccion === collection.id.toString())
                    return {
                        id: collection.id,
                        name: collection.nombre,
                        description: collection.descripcion,
                        caseId: collection.instancia_bonita,
                        finished: collection.terminada,
                        furniture: furniture,
                    }
                })
                this.collections = collections
                console.log(this.collections)
            } catch (error) {
                this.collections = { error }
            }
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
        },
    }
})
