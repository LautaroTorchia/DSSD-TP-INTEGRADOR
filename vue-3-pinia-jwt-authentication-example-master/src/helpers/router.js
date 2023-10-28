import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '@/stores'
import { HomeView, LoginView, CollectionListView, CollectionCreateView, CollectionUpdateView, FurnitureListView } from '@/views'


export const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    linkActiveClass: 'active',
    routes: [
        { path: '/', component: HomeView },
        { path: '/login', component: LoginView },
        { path: '/collections', component: CollectionListView, name : 'collections' },
        { path: '/collection/create', component: CollectionCreateView , name: 'collection-create' },
        { path: '/collection/:collection/update', component: CollectionUpdateView , name: 'collection-update' },
        { path: '/:collection/furniture', component: FurnitureListView, name: 'furniture' },
        { path: '/:collection/furniture/create', component: FurnitureCreateView , name: 'furniture-create' },
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
