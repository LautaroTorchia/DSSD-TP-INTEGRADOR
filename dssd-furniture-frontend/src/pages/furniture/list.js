import { useEffect, useState } from 'react';
import Navbar from '@/components/Navbar';
import PrivateLayout from '@/components/privateLayout';
import { useRouter } from 'next/router';
import createApiClient from '@/axios/axios';
import FurnitureList from '@/components/FurnitureList';


export default function ListFurniture() {
    const router = useRouter();
    const api = createApiClient();
    const { collectionid } = router.query;
    const collection = JSON.parse(localStorage.getItem(`${collectionid}`))
    const [furniture, setFurniture] = useState([]);

    const getAllFurniture = async () => {
        try {
            const response = await api.get('coleccion/muebles/');
            return response.data.results;
        } catch (error) {
            throw error;
        }
    };


    useEffect(() => {
        getAllFurniture()
            .then((data) => {
                const filteredFurniture = collectionid
                    ? data.filter((item) => item.coleccion === collection.id)
                    : data;
                setFurniture(filteredFurniture);
            })
            .catch((error) => {
                console.error('Error fetching furniture:', error);
            });
    }, [collectionid]);

    const handleReturn = () => {
        localStorage.removeItem(`${collectionid}`)
        router.push(`/collection/list`)
    }
    const handleUpdate = (furniture_item) => {
        localStorage.setItem(`${furniture_item.id}`, JSON.stringify(furniture_item))
        router.push(`/furniture/edit/${furniture_item.id}`)
    }
    const handleDelete = async (furniture_item) => {
        try {
            if (confirm(`¿Estás seguro que quieres borrar el mueble ${furniture_item.nombre}?`)) {
                const response = await api.delete(`/coleccion/muebles/${furniture_item.id}/`)
            }
        } catch (error) {
            throw error;
        }
    }
    return (
        <PrivateLayout>
            <div>
                <div>
                    <Navbar />
                </div>
                <h1>Muebles de {collection.name}</h1>
                <FurnitureList furniture={furniture} handleUpdate={handleUpdate} handleDelete={handleDelete} />
                <div onClick={() => handleReturn(collection)} >
                    Volver
                </div>
            </div>
        </PrivateLayout>
    );
}
