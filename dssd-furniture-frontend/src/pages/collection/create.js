import Navbar from '@/components/Navbar';
import CollectionForm from '@/components/CollectionForm'; // Import the CollectionForm component
import { useRouter } from 'next/router';
import { API_URL } from '@/../config';
import { listBonitaProcesses } from '@/endpoints/fetchProcesses';
import PrivateLayout from '@/components/privateLayout';
import { instantiateBonita } from '@/endpoints/instantiateProcess';

export default function CreateColeccionPage() {
  const router = useRouter();

  const handleSubmit = async (coleccionData) => {
    try {
      // Send a POST request to the /coleccion/muebles/ endpoint with the form data
      const response = await fetch(`${API_URL}coleccion/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(coleccionData),
      });

      if (response.ok) {
        const bonitaProcessesResponse = await listBonitaProcesses();
        const foundItem = bonitaProcessesResponse.find(item => item.displayName === "Muebles");
        const bonitaInstantiationResponse = instantiateBonita(foundItem.id, {
          "ticket_account": "string",
          "ticket_description": "string",
          "ticket_subject": "string"
        })
        console.log(bonitaInstantiationResponse);

        router.push('/collection/list')
      } else {
        console.error('Error:', response.statusText)
      }
    } catch (error) {
      console.error('Error:', error)
    }
  };

  return (
    <PrivateLayout>
      <div>
        <div>
          <Navbar />
        </div>
        <div>
          <h2>Crear Nueva Colección</h2>
          <CollectionForm onSubmit={handleSubmit} />
        </div>
      </div>
    </PrivateLayout>
  );
}