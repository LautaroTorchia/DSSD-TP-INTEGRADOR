import { defineStore } from 'pinia'

import { fetchWrapper, router } from '@/helpers'
import { jwtDecode } from 'jwt-decode'

const baseUrl = `${import.meta.env.VITE_API_URL}`

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        // initialize state from local storage to enable user to stay logged in
        user: JSON.parse(localStorage.getItem('user')),
        returnUrl: null
    }),
    getters: {
        isTokenExpired: (state) => {
            if (state.user) {
                const currentTime = Date.now() / 1000
                return jwtDecode(state.user.tokens.access).exp < currentTime
            }
            return true
        },
    },
    actions: {
        async login(email, password) {
            const user = await fetchWrapper.post(`${baseUrl}/auth/login/`, { email, password })

            // update pinia state
            this.user = user

            // store user details and jwt in local storage to keep user logged in between page refreshes
            localStorage.setItem('user', JSON.stringify(user))

            // redirect to previous url or default to home page
            router.push(this.returnUrl || '/')
        },
        logout() {
            this.user = null
            localStorage.removeItem('user')
            localStorage.clear()
            router.push('/login')
        }
    }
})
