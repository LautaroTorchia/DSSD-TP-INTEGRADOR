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

export async function getBonitaVariable(caseId, variableName) {
    try {
        const response = await fetchWrapper.get(`${baseUrl}/bonita/case-variable/${caseId}/${variableName}/`)
        if (response.value == "null") {
            throw new Error('Response data is empty')
        }
        return true
    } catch (error) {
        return false
    }
}