import { defineStore } from 'pinia';

import { fetchWrapper } from '@/helpers';

const baseUrl = `${import.meta.env.VITE_API_URL}`;

export const useUsersStore = defineStore({
    id: 'users',
    state: () => ({
        users: {}
    }),
    actions: {
        async getAll() {
            this.users = { loading: true }
            fetchWrapper.get(`${baseUrl}/auth/users`)
                .then(data => {
                    const users = data.results.map(user => {
                        return {
                            id: user.id,
                            email: user.email,
                            username: user.username
                        }
                    })
                    this.users = users
                })
                .catch(error => this.users = { error })
        }
    }
});
