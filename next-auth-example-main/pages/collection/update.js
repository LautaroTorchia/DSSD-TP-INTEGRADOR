import Navbar from '@/components/Navbar';
import CollectionForm from '@/components/CollectionForm';
import PrivateLayout from '@/components/privateLayout';
import createApiClient from "@/axios/axios";
import { useRouter } from 'next/router';



export default function UpdateColeccionPage() {
    const router = useRouter();
    const api = createApiClient();
    const { collectionid } = router.query;
    const collection = JSON.parse(localStorage.getItem(`${collectionid}`))

    const handleSubmit = async (collectionData) => {
        try {
            const response = await api.patch(`coleccion/${collectionid}/`, collectionData);
            if (response.status === 200) {
                localStorage.removeItem(`${collectionid}`)
                router.push('/collection/list')
            } else {
                console.error('Error:', response.statusText)
            }
            console.log('Edit Collection Success:', response.data);
        } catch (error) {
            console.error('Edit Collection Error:', error);
        }
    };

    return (
        <PrivateLayout>
          <div>
            <Navbar />
            <div className="container mt-4">
              <h2 className="mb-4">Editando Colección: {collection.nombre}</h2>
              <CollectionForm onSubmit={handleSubmit} collection={collection} />
            </div>
          </div>
        </PrivateLayout>
      );
    }