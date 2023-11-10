import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '@/stores'
import { Home, Login, CollectionList, CollectionCreate, CollectionUpdate, FurnitureList, FurnitureCreate, FurnitureDetail, DesignedCollectionList, MaterialAnalysis, FabricationPlan  } from '@/views'


export const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    linkActiveClass: 'active',
    routes: [
        { path: '/', component: Home, name: 'home' },
        { path: '/login', component: Login, name: 'login' },
        { path: '/collections', component: CollectionList, name : 'collections' },
        { path: '/collection/create', component: CollectionCreate , name: 'collection-create' },
        { path: '/collection/:collection/update', component: CollectionUpdate , name: 'collection-update' },
        { path: '/:collection/furniture', component: FurnitureList, name: 'furniture' },
        { path: '/:collection/furniture/create', component: FurnitureCreate , name: 'furniture-create' },
        { path: '/:collection/furniture/:id', component: FurnitureDetail , name: 'furniture-detail' },
        { path: '/designed-collections', component: DesignedCollectionList , name: 'designed-collections' },
        { path: '/:collection/material-analysis', component: MaterialAnalysis , name: 'material-analysis' },
        { path: '/:collection/fabrication-plan', component: FabricationPlan , name: 'fabrication-plan' },
    ]
})

router.beforeEach(async (to) => {
    // redirect to login page if not logged in and trying to access a restricted page
    const publicPages = ['/login']
    const authRequired = !publicPages.includes(to.path)
    const auth = useAuthStore()

    if (authRequired && !auth.user) {
        auth.returnUrl = to.fullPath
        return '/login'
    }
})
