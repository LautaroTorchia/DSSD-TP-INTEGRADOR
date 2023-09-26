import Navbar from '@/components/Navbar';
import CollectionForm from '../../components/CollectionForm'; // Import the CollectionForm component

export default function CreateCollectionPage() {
  return (
    <div>
      <div>
        <Navbar />
      </div>
      <div>
        <h2>Crear Nueva Colección</h2>
        <CollectionForm />
      </div>
  </div>
  );
}