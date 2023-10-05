import Navbar from '@/components/Navbar';
import FurnitureForm from '@/components/FurnitureForm';
import { useRouter } from 'next/router';
import PrivateLayout from '@/components/privateLayout';
import createApiClient from '@/axios/axios';


export default function UpdateFurniturenPage() {
    const router = useRouter();
    const api = createApiClient();
    const { collectionid } = router.query;
    const collection = JSON.parse(localStorage.getItem(`${collectionid}`))

    const handleSubmit = async (furnitureData) => {
        try {
            console.log("furnitureData")
            const response = await api.patch(`coleccion/muebles/`, furnitureData);
            if (response.status === 201) {
                localStorage.removeItem(`${collectionid}`)
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
                    <h2>Editar mueble</h2>
                    <FurnitureForm onSubmit={handleSubmit} collection={collection} />
                </div>
            </div>
        </PrivateLayout>
    );
}