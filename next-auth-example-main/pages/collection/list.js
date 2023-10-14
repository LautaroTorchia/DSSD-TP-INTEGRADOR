import { Button, Card, ListGroup } from 'react-bootstrap';
import { useEffect, useState } from 'react';
import Navbar from '@/components/Navbar';
import { API_URL } from '@/../config';
import PrivateLayout from '@/components/privateLayout';
import { useRouter } from 'next/router'; 
import createApiClient from '@/axios/axios';
import { executeBonitaTask, listBonitaUserTask } from '@/endpoints/usertask';
import { editCollection } from '@/endpoints/collection';
import { updateBonitaCaseVariable } from '@/endpoints/getvariable';

export default function CollectionList() {
  const [collections, setCollections] = useState([]);
  const [refreshCollections, setRefreshCollections] = useState(false);
  const router = useRouter();
  const api = createApiClient();

  useEffect(() => {
    const fetchCollections = async () => {
      try {
        const response = await api.get('coleccion/');
        console.log(response);
        if (response.status === 200) {
          setCollections(response.data.results);
        } else {
          console.error('Error:', response.statusText);
        }
      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchCollections();
  }, [refreshCollections]);

  const handleEdit = (collection) => {
    localStorage.setItem(`${collection.id}`, JSON.stringify(collection));
    router.push(`/collection/update?collectionid=${collection.id}`);
  };

  const handleAddFurniture = (collection) => {
    localStorage.setItem(`${collection.id}`, JSON.stringify(collection));
    router.push(`/furniture/create?collectionid=${collection.id}`);
  };

  const handleListFurniture = (collection) => {
    localStorage.setItem(`${collection.id}`, JSON.stringify(collection));
    router.push(`/furniture/list?collectionid=${collection.id}`);
  };

  const handleFinishCollection = async (collection) => {
    const UserTasksResponse = await listBonitaUserTask();

    const foundTask = UserTasksResponse.find(
      (task) => task.rootContainerId == collection.instancia_bonita
    );
    const ExecuteTaskResponse = await executeBonitaTask(foundTask.id, {
      ticket_comment: `Se ha ejecutado la tarea ${foundTask.displayName}`,
    });
    const UpdateBonitaCaseVariableResponse = await updateBonitaCaseVariable(
      collection.instancia_bonita,
      'collection_id',
      {
        type: 'java.lang.String',
        value: `${collection.id}`,
      }
    );
    console.log(collection.instancia_bonita);
    const UpdateCollectionResponse = await editCollection(collection.id, {
      terminada: 'true',
    });

    setRefreshCollections(true);
    router.push(`/collection/list`);
  };

  return (
    <PrivateLayout>
      <div>
        <div>
          <Navbar />
        </div>
        <h1 className="text-center mb-4 display-4 font-weight-bold">Colecciones</h1>
        <ListGroup>
          <div className="row mx-2">
            {collections.map((collection, index) => (
              <div key={collection.id} className="col-md-4 mb-3">
                <Card className={`h-100 ${index % 2 === 0 ? 'bg-light' : 'bg-light'}`}>
                  <Card.Body>
                    <h5 className="card-title">Nombre: {collection.nombre}</h5>
                    <p className="card-text">Descripcion: {collection.descripcion}</p>
                    <p className="card-text">Fecha creacion: {collection.fecha_creacion}</p>
                    <Button
                      variant="outline-primary"
                      onClick={() => handleEdit(collection)}
                      className="btn-block mb-2"
                      disabled={collection.terminada}
                    >
                      Editar
                    </Button>
                    <Button
                      variant="outline-success"
                      onClick={() => handleAddFurniture(collection)}
                      className="btn-block mb-2"
                      disabled={collection.terminada}
                    >
                      Añadir mueble 
                    </Button>
                    <Button
                      variant="outline-info"
                      onClick={() => handleListFurniture(collection)}
                      className="btn-block mb-2"
                    >
                      Ver muebles
                    </Button>
                    {!collection.terminada ? (
                      <Button
                        variant="outline-danger"
                        onClick={() => handleFinishCollection(collection)}
                        className="btn-block mb-2"
                      >
                        Terminar diseño
                      </Button>
                    ) : (
                      <Button
                        variant="outline-danger"
                        className="btn-block disabled mb-2"
                        disabled
                      >
                        Diseñado
                      </Button>
                    )}
                  </Card.Body>
                </Card>
              </div>
            ))}
          </div>
        </ListGroup>
      </div>
    </PrivateLayout>
  );
}
