import { defineStore } from 'pinia'

export function useMaterialListStore(initialList){
    const materialListStore = defineMaterialListStore()
    if (initialList){
        materialListStore.addMaterialList(initialList)
    }
    return materialListStore
}

 const defineMaterialListStore = defineStore({
    id: 'materialList',
    persist: true, 
    state: () => ({
        materialList: []
    }),
    getters: {
        getMaterials: state => state.materialList
    },
    actions: {
        addMaterialList(newMaterialList) {
            const index = this.materialList.findIndex(materialList => materialList.id === newMaterialList.id)
            if (index === -1) {
                this.materialList.push(newMaterialList)
            } else {
                this.materialList.splice(index, 1, newMaterialList)
            }
        },
    },
})