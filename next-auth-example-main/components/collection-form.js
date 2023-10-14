import { useState } from 'react';

export default function CollectionForm({ onSubmit, collection }) {
  if (!collection) {
    collection = {
      nombre: '',
      descripcion: '',
    };
  }
  const [nombre, setNombre] = useState(collection.nombre);
  const [descripcion, setDescripcion] = useState(collection.descripcion);

  const handleSubmit = (e) => {
    e.preventDefault();

    const collectionData = {
      nombre,
      descripcion,
      terminada: false,
      instancia_bonita: null,
    };

    onSubmit(collectionData);
  };

  return (
    <form onSubmit={handleSubmit} className="rounded p-4 border">
      <div className="form-group">
        <label htmlFor="nombre">Nombre:</label>
        <input
          type="text"
          id="nombre"
          className="form-control"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="descripcion">Descripción:</label>
        <textarea
          id="descripcion"
          className="form-control"
          value={descripcion}
          onChange={(e) => setDescripcion(e.target.value)}
          rows="5"
          required
        ></textarea>
      </div>
      <div className="text-center">
        <button type="submit" className="btn btn-primary btn-lg">
          Guardar
        </button>
      </div>
    </form>
  );
}

