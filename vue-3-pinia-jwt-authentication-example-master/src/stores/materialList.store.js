import { defineStore } from 'pinia'

export function useMaterialListStore(initialList){
    const materialListStore = defineMaterialListStore()
    materialListStore.setMaterials(initialList)
    return materialListStore
}

 const defineMaterialListStore = defineStore({
    id: 'materialList',
    state: () => ({
        materials: []
    }),
    getters: {
        getMaterials: state => state.materials
    },
    actions: {
        addMaterial(material) {
            this.materials.push(material)
        }
    },
    setMaterials(materials) {
        this.materials = materials
    },
})

