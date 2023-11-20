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
export const GetBonitaTask = async (caseId) => {
    const tasks = await fetchWrapper.get(`${baseUrl}/bonita/user-tasks/`)
    const task = tasks.filter(task => task.rootCaseId === caseId.toString())
    return task
}

export async function advanceNamedBonitaTask(caseId, taskName) {
    const tasks = await fetchWrapper.get(`${baseUrl}/bonita/user-tasks/`)
    console.log(tasks,caseId,taskName)
    const task = tasks.find(task => task.caseId === caseId.toString() && task.name === taskName || console.log(task.name,taskName))
    console.log(task)
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
        return response.value
    } catch (error) {
        return false
    }
}

export async function setBonitaVariable(caseId, variableName, variableValue) {
    try {
        const value = typeof variableValue === 'object' ? JSON.stringify(variableValue) : variableValue;
        const response = await fetchWrapper.put(`${baseUrl}/bonita/update-case-variable/${caseId}/${variableName}/`, { type: "java.lang.String", value })
        return response.value
    } catch (error) {
        return error
    }
}

//TODO: make patchBonitaVariable it retrieves the variable and then updates it
export async function patchBonitaVariable(caseId, variableName,fieldname, fieldValue) {
    try {
        const field = typeof fieldValue === 'string' ? JSON.parse(fieldValue) : fieldValue;
        const value = JSON.parse(await getBonitaVariable(caseId, variableName))
        value[fieldname] = field
        console.log(value)
        const response = await fetchWrapper.put(`${baseUrl}/bonita/update-case-variable/${caseId}/${variableName}/`, { type: "java.lang.String", value })
        return response.value
    } catch (error) {
        return error
    }
}

