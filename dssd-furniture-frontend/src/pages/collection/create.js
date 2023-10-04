import Navbar from '@/components/Navbar';
import CollectionForm from '@/components/CollectionForm'; // Import the CollectionForm component
import { useRouter } from 'next/router';
import { API_URL } from '@/../config';
import { loginToBonita } from '@/endpoints/bonitalogin';
import { listBonitaProcesses } from '@/endpoints/fetchProcesses';

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

        //Here we should continue with BONITA ENDPOINTS
        const bonitaLoginResponse = await loginToBonita('anthony.nichols', 'bpm');
        console.log(bonitaLoginResponse)

        const bonitaProcessesResponse = await listBonitaProcesses();
        console.log(bonitaProcessesResponse)


        router.push('/collection/list');
      } else {
        // Handle error cases
        console.error('Error:', response.statusText);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <div>
        <Navbar />
      </div>
      <div>
        <h2>Crear Nueva Colección</h2>
        <CollectionForm onSubmit={handleSubmit} />
      </div>
  </div>
  );
}