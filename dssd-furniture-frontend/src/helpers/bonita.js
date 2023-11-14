import { fetchWrapper } from '@/helpers'
const baseUrl = `${import.meta.env.VITE_API_URL}`

export const advanceBonitaTask = async (caseId) => {
    const tasks = await fetchWrapper.get(`${baseUrl}/bonita/user-tasks/`)
    const task = tasks.find(task => task.rootCaseId === caseId.toString())
    if (!task) {
        throw new Error('No se encontró la tarea')
    }
    await fetchWrapper.post(`${baseUrl}/bonita/execute-user-task/${task.id}/`)
}