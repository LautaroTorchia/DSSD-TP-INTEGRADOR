import Navbar from '@/components/Navbar';
import CollectionForm from '@/components/CollectionForm'; // Import the CollectionForm component
import { useRouter } from 'next/router';
import { API_URL } from '@/../config';

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
        // Redirect to a success page or perform any other actions
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