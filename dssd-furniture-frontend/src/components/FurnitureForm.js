import { useState } from 'react';

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
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-6">
            <form onSubmit={handleSubmit(furnitureData)} className="mb-4 p-5 border rounded">
              <div className="mb-3">
                <label htmlFor="nombre" className="form-label text-primary fw-bold">
                  Nombre:
                </label>
                <input
                  type="text"
                  id="nombre"
                  name="nombre"
                  value={furnitureData.nombre}
                  onChange={handleChange}
                  className="form-control rounded-pill"
                  required
                />
              </div>
  
              <div className="mb-3">
                <label htmlFor="plazo_fabricacion" className="form-label text-primary fw-bold">
                  Plazo de Fabricación (días):
                </label>
                <input
                  type="number"
                  id="plazo_fabricacion"
                  name="plazo_fabricacion"
                  value={furnitureData.plazo_fabricacion}
                  onChange={handleChange}
                  className="form-control rounded-pill"
                  required
                />
              </div>
  
              <div className="mb-3">
                <label htmlFor="fecha_lanzamiento_estimada" className="form-label text-primary fw-bold">
                  Fecha de Lanzamiento Estimada:
                </label>
                <input
                  type="date"
                  id="fecha_lanzamiento_estimada"
                  name="fecha_lanzamiento_estimada"
                  value={furnitureData.fecha_lanzamiento_estimada}
                  onChange={handleChange}
                  className="form-control rounded-pill"
                  required
                />
              </div>
  
              <div className="mb-3">
                <label htmlFor="descripcion" className="form-label text-primary fw-bold">
                  Descripción:
                </label>
                <textarea
                  id="descripcion"
                  name="descripcion"
                  value={furnitureData.descripcion}
                  onChange={handleChange}
                  className="form-control rounded-pill"
                  required
                />
              </div>
  
              <div className="mb-3">
                <label htmlFor="imagen" className="form-label text-primary fw-bold">
                  Imagen (URL):
                </label>
                <input
                  type="url"
                  id="imagen"
                  name="imagen"
                  value={furnitureData.imagen}
                  onChange={handleChange}
                  className="form-control rounded-pill"
                />
              </div>
  
              <div className="mb-3">
                <label htmlFor="plan_fabricacion" className="form-label text-primary fw-bold">
                  Plan de Fabricación (URL):
                </label>
                <input
                  type="url"
                  id="plan_fabricacion"
                  name="plan_fabricacion"
                  value={furnitureData.plan_fabricacion}
                  onChange={handleChange}
                  className="form-control rounded-pill"
                />
              </div>
  
              <div className="mb-3">
                <label htmlFor="materiales" className="form-label text-primary fw-bold">
                  Materiales:
                </label>
                <textarea
                  id="materiales"
                  name="materiales"
                  value={furnitureData.materiales}
                  onChange={handleChange}
                  className="form-control rounded-pill"
                />
              </div>
  
              <button type="submit" className="btn btn-primary btn-lg">
                Crear mueble
              </button>
            </form>
          </div>
        </div>
      </div>
    );
  };
  
  export default FurnitureForm;