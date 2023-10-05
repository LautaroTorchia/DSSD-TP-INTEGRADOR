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
    localStorage.setItem(`${collection.id}`, JSON.stringify(collection))
    router.push(`/collection/update?collectionid=${collection.id}`)
  }

  const handleAddFurniture = (collection) => {
    localStorage.setItem(`${collection.id}`, JSON.stringify(collection))
    router.push(`/furniture/create?collectionid=${collection.id}`)
  }

  const handleListFurniture = (collection) => {
    localStorage.setItem(`${collection.id}`, JSON.stringify(collection))
    router.push(`/furniture/list?collectionid=${collection.id}`)
  }

  const handleFinishCollection = async (collection) => {
    const UserTasksResponse = await listBonitaUserTask()

    const foundTask = UserTasksResponse.find(task => task.rootContainerId == collection.instancia_bonita);
    const ExecuteTaskResponse = await executeBonitaTask(foundTask.id,{
      "ticket_comment": `Se ha ejecutado la tarea ${foundTask.displayName}`
    })
    const UpdateBonitaCaseVariableResponse = await updateBonitaCaseVariable(collection.instancia_bonita,"collection_id",{
      "type": "java.lang.String",
      "value":`${collection.id}`
    })
    console.log(collection.instancia_bonita)
    const UpdateCollectionResponse = await editCollection(collection.id,{"terminada":"true"})

    setRefreshCollections(true);
    router.push(`/collection/list`)
  }


  return (
    <PrivateLayout>
      <div>
        <div>
          <Navbar />
        </div>
        <h1>Collection List</h1>
        <ul>
          {collections.map((collection) => (
            <div>
              <li key={collection.id}>
                <h2>{collection.nombre}</h2>
                <p>{collection.descripcion}</p>
                <p>{collection.fecha_creacion}</p>
              </li>
              <div onClick={() => handleEdit(collection) } >
              Editar {collection.nombre}
              </div>
              <div onClick={() => handleAddFurniture(collection) } >
              Agregar mueble {collection.nombre}
              </div>
              <div onClick={() => handleListFurniture(collection) } >
              Ver muebles {collection.nombre}
              </div>
              {!collection.terminada ? (
                <div onClick={() => handleFinishCollection(collection)}>
                  Finalizar coleccion {collection.nombre}
                </div>
              ) : null}

            </div>
          ))}
        </ul>
      </div>
    </PrivateLayout>
  );
}
