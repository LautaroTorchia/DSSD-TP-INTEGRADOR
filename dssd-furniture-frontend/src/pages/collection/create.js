import Navbar from '@/components/Navbar';
import CollectionForm from '@/components/CollectionForm'; // Import the CollectionForm component
import { useRouter } from 'next/router';
import { API_URL } from '@/../config';
import { listBonitaProcesses } from '@/endpoints/fetchProcesses';
import PrivateLayout from '@/components/privateLayout';
import { instantiateBonita } from '@/endpoints/instantiateProcess';
import createApiClient from '@/axios/axios';

export default function CreateColeccionPage() {
  const router = useRouter();
  const api = createApiClient();

  const handleSubmit = async (coleccionData) => {
    try {

      const bonitaProcessesResponse = await listBonitaProcesses();
      const foundItem = bonitaProcessesResponse.find(item => item.displayName === "Muebles");
      const bonitaInstantiationResponse = await instantiateBonita(foundItem.id, {
        "ticket_account": "string",
        "ticket_description": "string",
        "ticket_subject": "string"
      })
      console.log(bonitaInstantiationResponse.data)
      console.log(bonitaInstantiationResponse.data.caseId)
      coleccionData.instancia_bonita = bonitaInstantiationResponse.data.caseId
      console.log(coleccionData)
      const response = await api.post(`${API_URL}coleccion/`, JSON.stringify(coleccionData))
      router.push('/collection/list')
    } catch (error) {
      console.error('Error:', error)
    }
  };

  return (
    <PrivateLayout>
      <div>
        <Navbar />
        <div className="container mt-5">
        <h1 className="text-center mb-4 display-4 font-weight-bold">Crear nueva coleccion</h1>
          <div className="row justify-content-center">
            <div className="col-md-6">
              <CollectionForm onSubmit={handleSubmit} />
            </div>
          </div>
        </div>
      </div>
    </PrivateLayout>
  );
}