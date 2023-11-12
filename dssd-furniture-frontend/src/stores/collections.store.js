import { defineStore } from 'pinia'
import { useFurnitureStore } from './furniture.store'
import { fetchWrapper } from '@/helpers'

const baseUrl = `${import.meta.env.VITE_API_URL}`


const createBonitaInstance = async () => {
    const responseListProcesses = await fetchWrapper.get(`${baseUrl}/bonita/list-processes/`)
    const processId = responseListProcesses[0].id
    const response = await fetchWrapper.post(`${baseUrl}/bonita/instantiate/${processId}/`)
    return response.caseId
}

const advanceBonitaTask = async (caseId) => {
    const tasks = await fetchWrapper.get(`${baseUrl}/bonita/user-tasks/`)
    const task = tasks.find(task => task.rootCaseId === caseId.toString())
    if (!task) {
        throw new Error('No se encontró la tarea')
    }
    await fetchWrapper.post(`${baseUrl}/bonita/execute-user-task/${task.id}/`)
}

export const useCollectionsStore = defineStore({
    id: 'collections',
    state: () => ({
        collections: {}
    }),
    persist: true,//https://prazdevs.github.io/pinia-plugin-persistedstate/guide/config.html
    getters: {
        getCollections: (state) => {
            return state.collections
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
                        created_at: collection.fecha_creacion,
                        estimated_launch_date: collection.fecha_lanzamiento_estimada,
                        caseId: collection.instancia_bonita,
                        designed: collection.diseñada,
                        furniture: furniture,
                    }
                }))
                this.collections = collections
                return collections
            } catch (error) {
                this.collections = { error }
            }
        },
        getById(id) {
            return this.collections.find(collection => collection.id == id)
        },
        async delete(id) {
            try {
                await fetchWrapper.delete(`${baseUrl}/coleccion/${id}/`)
                this.collections.splice(this.collections.findIndex(collection => collection.id === id), 1)
            } catch (error) {
                this.collections = { error }
            }
        },
        async create(values) {
            this.collections = { loading: true }
            const data = {
                nombre: values.name,
                descripcion: values.description,
                fecha_lanzamiento_estimada: values.estimated_release,
            }
            const response = await fetchWrapper.post(`${baseUrl}/coleccion/`, data).catch(error => this.collections = { error })
            const caseId = await createBonitaInstance()
            const patchResponse = await fetchWrapper.patch(`${baseUrl}/coleccion/${response.id}/`, { instancia_bonita: caseId }).catch(error => this.collections = { error })
        },
        async finish(collection) {
            collection.designed = true
            try {
                await advanceBonitaTask(collection.caseId)
                await fetchWrapper.patch(`${baseUrl}/coleccion/${collection.id}/`, { diseñada: true })
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
