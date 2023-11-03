<template>
    <form @submit.prevent="submitForm">
        <div class="collection-details">
            <div class="collection-info">
                <h2><input v-model="collection.name" type="text"></h2>
                <p><input v-model="collection.description" type="text"></p>
            </div>
            <div class="furniture-list">
                <div class="furniture-item" v-for="furniture in furnitureList" :key="furniture.id">
                    <h3>{{ furniture.name }}</h3>
                    <div class="material-list">
                        <div class="material-item" v-for="material in furniture.materials" :key="material.id">
                            <label>{{ material.name }}</label>
                            <input type="number" v-model="material.quantity">
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <button type="submit">Submit</button>
    </form>
</template>

<script>
export default {
    name: 'CollectionDetails',
    props: {
        collection: {
            type: Object,
            default: {
                name: 'Living Room Collection',
                description: 'A collection of furniture for the living room'
            }
        },
        furnitureList: {
            type: Array,
            default: () => [
                {
                    id: 1,
                    name: 'Sofa',
                    materials: [
                        { id: 1, name: 'Fabric', quantity: 5 },
                        { id: 2, name: 'Wood', quantity: 10 }
                    ]
                },
                {
                    id: 2,
                    name: 'Coffee Table',
                    materials: [
                        { id: 3, name: 'Glass', quantity: 1 },
                        { id: 4, name: 'Metal', quantity: 3 }
                    ]
                }
            ]
        }
    },
    methods: {
        submitForm() {
            console.log(this.collection)
            console.log(this.furnitureList)
        }
    }
}
</script>
