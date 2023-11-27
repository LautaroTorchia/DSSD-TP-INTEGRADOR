import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '@/stores'
import { Home, Login, CollectionList, CollectionCreate, CollectionUpdate, FurnitureList, FurnitureCreate, FurnitureDetail, DesignedCollectionList, MaterialAnalysis, FabricationPlan, FabricationPlanConfirm, Dashboard, DeliveryOrderList, MaterialControl, DeliveryOrderCreate, FabricationControlList, Renegociate, DistributionList, DistributionCreate } from '@/views'

import ForbiddenPage from '@/views/forbidden.vue';
import { FabricationControl } from '../views'
import { fetchWrapper } from '../helpers'

export const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    linkActiveClass: 'active',
    routes: [
        { path: '/', component: Home, name: 'home' },
        { path: '/forbidden', component: ForbiddenPage, name: 'forbidden' },
        { path: '/login', component: Login, name: 'login' },
        { path: '/dashboard', component: Dashboard, name: 'dashboard', meta: { roles: ['admin'] } },

        { path: '/collections', component: CollectionList, name: 'collections', meta: { roles: ['designer', 'admin'] } },
        { path: '/collection/create', component: CollectionCreate, name: 'collection-create', meta: { roles: ['designer', 'admin'] } },
        { path: '/collection/:collection/update', component: CollectionUpdate, name: 'collection-update', meta: { roles: ['designer', 'admin'] } },
        { path: '/:collection/furniture', component: FurnitureList, name: 'furniture', meta: { roles: ['designer', 'admin'] } },
        { path: '/:collection/furniture/create', component: FurnitureCreate, name: 'furniture-create', meta: { roles: ['designer', 'admin'] } },
        { path: '/:collection/furniture/:id', component: FurnitureDetail, name: 'furniture-detail', meta: { roles: ['designer', 'admin'] } },

        { path: '/designed-collections', component: DesignedCollectionList, name: 'designed-collections', meta: { roles: ['operations_analist', 'admin'] } },
        { path: '/:collection/material-analysis', component: MaterialAnalysis, name: 'material-analysis', meta: { roles: ['operations_analist', 'admin'] } },
        { path: '/:collection/fabrication-plan', component: FabricationPlan, name: 'fabrication-plan', meta: { roles: ['operations_analist', 'admin'] } },
        { path: '/:collection/fabrication-plan-confirm', component: FabricationPlanConfirm, name: 'fabrication-plan-confirm', meta: { roles: ['operations_analist', 'admin'] } },
        { path: '/:collection/material-control', component: MaterialControl, name: 'material-control-list', meta: { roles: ['operations_analist', 'admin'] } },
        { path: '/:collection/renegociate', component: Renegociate, name: 'renegociate-collection', meta: { roles: ['operations_analist', 'admin'] } },
        { path: '/distribution-list', component: DistributionList, name: 'distribution-list', meta: { roles: ['operations_analist', 'admin'] } },
        { path: '/:collection/distribution-create', component: DistributionCreate, name: 'distribution-create', meta: { roles: ['operations_analist', 'admin'] } },

        { path: '/fabrication-control-list', component: FabricationControlList, name: 'fabrication-control-list', meta: { roles: ['factory_liason', 'admin'] } },
        { path: '/:collection/fabrication-control', component: FabricationControl, name: 'fabrication-control', meta: { roles: ['factory_liason', 'admin'] } },

        { path: '/delivery-order-collection-list', component: DeliveryOrderList, name: 'delivery-order-collection-list', meta: { roles: ['commercial_analist', 'admin'] } },
        { path: '/:collection/delivery-order-create', component: DeliveryOrderCreate, name: 'delivery-order-create', meta: { roles: ['commercial_analist', 'admin'] } },
    ]
})

router.beforeEach(async (to, from, next) => {
    const publicPages = ['/login', '/forbidden', "/"]; // Exclude /forbidden from authentication check
    const authRequired = !publicPages.includes(to.path)
    const auth = useAuthStore()

    // Check if the route requires authentication
    if (authRequired && auth.isTokenExpired) {
        return next('/login')
    }

    // Check user role for restricted routes
    if (authRequired) {
        try {
            const response = await fetchWrapper.get(`${import.meta.env.VITE_API_URL}/authorization/user-role`)
            const userRoles = response.map((role) => role.role_denomination)

            const allowedRoles = getAllowedRoles(to.meta)
            console.log("allowed roles in that view: ", allowedRoles)

            const storedUsername = JSON.parse(localStorage.getItem('user')).username;
            const matchingRoles = response.filter((role) => role.username === storedUsername)
            const hasAllowedRole = matchingRoles.some((role) => allowedRoles.includes(role.role_denomination))
            if (hasAllowedRole) {
                return next()
            } else {
                return next('/forbidden')
            }
        } catch (error) {
            console.error(error)
            // Redirect to login if there is an error fetching user roles
            return next('/login')
        }
    }

    // Continue to the next route
    next()
})

function getAllowedRoles(routeMeta) {
    // Retrieve the allowed roles from the route meta or provide a default value
    return routeMeta.roles || [];
}
