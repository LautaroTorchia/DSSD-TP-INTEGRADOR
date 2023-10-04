import { useState } from 'react';
import axios from 'axios';

const FurnitureForm = ({ onSubmit, collection }) => {
  const [furnitureData, setfurnitureData] = useState({
    nombre: '',
    coleccion: collection.id,
    plazo_fabricacion: '',
    fecha_lanzamiento_estimada: '',
    descripcion: '',
    imagen: '',
    plan_fabricacion: '',
    materiales: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setfurnitureData({
      ...furnitureData,
      [name]: value,
    });
  };

  const handleSubmit = (furnitureData) => async (e) => {
    e.preventDefault();
    onSubmit(furnitureData)
    }


  return (
    <form onSubmit={handleSubmit(furnitureData)}>
      <label>
        Nombre:
        <input type="text" name="nombre" value={furnitureData.nombre} onChange={handleChange} />
      </label>

      <label>
        Plazo de Fabricación (días):
        <input type="number" name="plazo_fabricacion" value={furnitureData.plazo_fabricacion} onChange={handleChange} />
      </label>

      <label>
        Fecha de Lanzamiento Estimada:
        <input type="date" name="fecha_lanzamiento_estimada" value={furnitureData.fecha_lanzamiento_estimada} onChange={handleChange} />
      </label>

      <label>
        Descripción:
        <textarea name="descripcion" value={furnitureData.descripcion} onChange={handleChange} />
      </label>

      <label>
        Imagen (URL):
        <input type="url" name="imagen" value={furnitureData.imagen} onChange={handleChange} />
      </label>

      <label>
        Plan de Fabricación (URL):
        <input type="url" name="plan_fabricacion" value={furnitureData.plan_fabricacion} onChange={handleChange} />
      </label>

      <label>
        Materiales:
        <textarea name="materiales" value={furnitureData.materiales} onChange={handleChange} />
      </label>

      <button type="submit">Create Furniture</button>
    </form>
  );
};

export default FurnitureForm;