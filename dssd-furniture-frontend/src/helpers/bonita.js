import { fetchWrapper } from "@/helpers";
const baseUrl = `${import.meta.env.VITE_API_URL}`;

export const advanceBonitaTask = async (caseId) => {
  const tasks = await fetchWrapper.get(`${baseUrl}/bonita/user-tasks/`);
  const task = tasks.find((task) => task.rootCaseId === caseId.toString());
  if (!task) {
    throw new Error("No se encontró la tarea");
  }
  await fetchWrapper.post(`${baseUrl}/bonita/execute-user-task/${task.id}/`);
};
export const getBonitaTask = async (caseId) => {
  const tasks = await fetchWrapper.get(`${baseUrl}/bonita/user-tasks/`);
  const task = tasks.filter((task) => task.rootCaseId === caseId.toString());
  return task;
};

export const getBonitaTasks = async () => {
  return await fetchWrapper.get(`${baseUrl}/bonita/asks/`);
};

export async function advanceNamedBonitaTaskWithCollection(
  collectionId,
  taskName,
) {
  const caseId = (
    await fetchWrapper.get(`${baseUrl}/coleccion/${collectionId}/`)
  ).instancia_bonita;
  await advanceNamedBonitaTask(caseId, taskName);
}

export async function advanceNamedBonitaTask(caseId, taskName) {
  const tasks = await fetchWrapper.get(`${baseUrl}/bonita/user-tasks/`);
  const task = tasks.find(
    (task) => task.caseId === caseId.toString() && task.name === taskName,
  );
  if (!task) {
    throw new Error("No se encontró la tarea");
  }
  try {
    await fetchWrapper.post(`${baseUrl}/bonita/execute-user-task/${task.id}/`);
  } catch (error) {
    throw new Error("No se pudo avanzar la tarea");
  }
}

export async function getBonitaVariable(caseId, variableName) {
  try {
    const response = await fetchWrapper.get(
      `${baseUrl}/bonita/case-variable/${caseId}/${variableName}/`,
    );
    if (response.value == "null") {
      throw new Error("Response data is empty");
    }
    return response.value;
  } catch (error) {
    return false;
  }
}

export async function setBonitaVariable(caseId, variableName, variableValue) {
  try {
    const value =
      typeof variableValue === "object"
        ? JSON.stringify(variableValue)
        : variableValue;
    const response = await fetchWrapper.put(
      `${baseUrl}/bonita/update-case-variable/${caseId}/${variableName}/`,
      { type: "java.lang.String", value },
    );
    return response.value;
  } catch (error) {
    return error;
  }
}

export async function patchBonitaVariable(
  caseId,
  variableName,
  fieldname,
  fieldValue,
) {
  try {
    const field =
      typeof fieldValue === "string" ? JSON.parse(fieldValue) : fieldValue;
    const value = JSON.parse(await getBonitaVariable(caseId, variableName));
    value[fieldname] = field;
    const response = await fetchWrapper.put(
      `${baseUrl}/bonita/update-case-variable/${caseId}/${variableName}/`,
      { type: "java.lang.String", value },
    );
    return response.value;
  } catch (error) {
    return error;
  }
}
