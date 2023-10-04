import { useEffect, useState } from 'react';
import Navbar from '@/components/Navbar';
import { API_URL } from '@/../config';
import PrivateLayout from '@/components/privateLayout';


export default function CollectionList() {
  const [collections, setCollections] = useState([]);

  useEffect(() => {
    const fetchCollections = async () => {
      try {
        const response = await fetch(`${API_URL}coleccion/`);
        if (response.ok) {
          const data = await response.json();
          setCollections(data.results);
        } else {
          console.error('Error:', response.statusText);
        }
      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchCollections();
  }, []);

  return (
    <PrivateLayout>
    <div>
      <div>
        <Navbar />
      </div>
      <h1>Collection List</h1>
      <ul>
        {collections.map((collection) => (
          <li key={collection.id}>
            <h2>{collection.nombre}</h2>
            <p>{collection.descripcion}</p>
            <p>{collection.fecha_creacion}</p>
          </li>
        ))}
      </ul>
    </div>
    </PrivateLayout>
  );
}
