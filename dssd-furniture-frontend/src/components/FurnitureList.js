import styled from 'styled-components';

const FurnitureListWrapper = styled.div`
  background-color: #000; /* Black background */
  color: #fff; /* White text color */
  padding: 20px;
`;

const FurnitureItem = styled.div`
  border: 1px solid #fff; /* White border */
  padding: 10px;
  margin-bottom: 10px;
`;

const FurnitureList = ({ furniture ,handleUpdate,handleDelete}) => {
    return (
        <FurnitureListWrapper>
            <h1>Furniture List</h1>
            {furniture.map((item) => (
                <FurnitureItem key={item.id}>
                    <h2>{item.nombre}</h2>
                    <p>Descripción: {item.descripcion}</p>
                    <p>Plazo de Fabricación: {item.plazo_fabricacion} días</p>
                    <p>Fecha de Lanzamiento Estimada: {item.fecha_lanzamiento_estimada}</p>
                    <p>Imagen: <img src={item.imagen} alt="Furniture" /></p>
                    <p>Plan de Fabricación: <a href={item.plan_fabricacion} target="_blank" rel="noopener noreferrer">Link</a></p>
                    <p>Materiales: {item.materiales}</p>
                    <div onClick={() => handleUpdate(item)} >
                        Editar
                    </div>
                    <div onClick={() => handleDelete(item)} >
                        Borrar
                    </div>
                </FurnitureItem>
            ))}
        </FurnitureListWrapper>
    );
};

export default FurnitureList;