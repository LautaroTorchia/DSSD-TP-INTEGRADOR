import CollectionForm from '@/components/collection-form'
import { useRouter } from 'next/router'
import { listBonitaProcesses } from '../api/endpoints/fetchProcesses'
import Layout from '@/components/layout'
import { instantiateBonita } from '../api/endpoints/instantiateProcess'
import axios from 'axios'
import { useSession } from "next-auth/react"

export default function CreateColeccionPage() {
  const { data } = useSession()
  console.log("data", data)
  if (data) {

    const router = useRouter();
    const api = axios.create({
      baseURL: `${process.env.API_URL}`,
      headers: {
        Authorization: `Bearer ${data.accessToken}`,
        'Content-Type': 'application/json',
      },

    })
  }


  const handleSubmit = async (coleccionData) => {
    try {
      const bonitaProcessesResponse = await listBonitaProcesses();
      const foundItem = bonitaProcessesResponse.find(item => item.displayName === "Muebles");
      const bonitaInstantiationResponse = await instantiateBonita(foundItem.id, {
        "ticket_account": "string",
        "ticket_description": "string",
        "ticket_subject": "string"
      })
      coleccionData.instancia_bonita = bonitaInstantiationResponse.data.caseId
      const response = await api.post(`${process.env.API_URL}/coleccion/`, JSON.stringify(coleccionData))
      router.push('/collection/list')
    } catch (error) {
      console.error('Error:', error)
    }
  };

  return (
    <Layout>
      <div>
        <div className="container mt-5">
          <h1 className="text-center mb-4 display-4 font-weight-bold">Crear nueva coleccion</h1>
          <div className="row justify-content-center">
            <div className="col-md-6">
              <CollectionForm onSubmit={handleSubmit} />
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}