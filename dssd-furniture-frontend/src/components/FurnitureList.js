import styled from 'styled-components';

const FurnitureListWrapper = styled.div`
  background-color: #f0f0f0;
  color: #333;
  padding: 20px;
`;

const FurnitureItem = styled.div`
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const FurnitureImage = styled.img`
  max-width: 100%;
  height: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-top: 10px;
`;

const FurnitureLink = styled.a`
  color: #007bff;
  text-decoration: none;
  &:hover {
    text-decoration: underline;
  }
`;

const FurnitureParagraph = styled.p`
  margin: 10px 0;
  font-size: 16px;
`;

const FurnitureLabel = styled.label`
  display: block;
  font-weight: bold;
  font-size: 18px;
  margin-bottom: 5px;
  color: #333;
`;

const FurnitureField = styled.div`
  margin: 10px 0;
`;

const FurnitureList = ({ furniture, handleUpdate, handleDelete }) => {
  return (
    <FurnitureListWrapper>
      <h1>Furniture List</h1>
      {furniture.map((item) => (
        <FurnitureItem key={item.id}>
          <h2>{item.nombre}</h2>
          <FurnitureField>
            <FurnitureLabel>Descripción:</FurnitureLabel>
            <FurnitureParagraph>{item.descripcion}</FurnitureParagraph>
          </FurnitureField>
          <FurnitureField>
            <FurnitureLabel>Plazo de Fabricación:</FurnitureLabel>
            <FurnitureParagraph>{item.plazo_fabricacion} días</FurnitureParagraph>
          </FurnitureField>
          <FurnitureField>
            <FurnitureLabel>Fecha de Lanzamiento Estimada:</FurnitureLabel>
            <FurnitureParagraph>{item.fecha_lanzamiento_estimada}</FurnitureParagraph>
          </FurnitureField>
          <FurnitureField>
            <FurnitureLabel>Imagen:</FurnitureLabel>
            <FurnitureImage src={item.imagen} alt="Furniture" />
          </FurnitureField>
          <FurnitureField>
            <FurnitureLabel>Plan de Fabricación:</FurnitureLabel>
            <FurnitureParagraph>
              <FurnitureLink href={item.plan_fabricacion} target="_blank" rel="noopener noreferrer">Link</FurnitureLink>
            </FurnitureParagraph>
          </FurnitureField>
          <FurnitureField>
            <FurnitureLabel>Materiales:</FurnitureLabel>
            <FurnitureParagraph>{item.materiales}</FurnitureParagraph>
          </FurnitureField>
          <button onClick={() => handleUpdate(item)} className="btn btn-primary">Editar</button>
          <button onClick={() => handleDelete(item)} className="btn btn-danger">Borrar</button>
        </FurnitureItem>
      ))}
    </FurnitureListWrapper>
  );
};

export default FurnitureList;
