<template>
    <div>
        <h1>Material Analysis</h1>
        <h2>{{ furniture }}</h2>
        <div v-for="(furniture, index) in furniture" :key="index">
            <div v-for="(material, index) in furniture.materials" :key="index">
                <label>{{ material.name }}:</label>
                <input type="number" v-model="material.quantity" />
            </div>
        </div>
    </div>
</template>

<script>
import { computed } from 'vue';
import { useCollectionsStore } from '@/stores'
import { router } from '@/helpers'

export default {
    props: {
    },
    setup(props) {
        const collectionsStore = useCollectionsStore()
        const furniture = computed(async () => {
            return await collectionsStore.getAll()
        })
        return {
            furniture,
        };
    },
};
</script>
