import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import { router } from './helpers'

import piniaPluginPersistedState from "pinia-plugin-persistedstate"
import  BackButton  from '@/components/BackButton.vue'
import ConfirmationService from 'primevue/confirmationservice';
import PrimeVue from 'primevue/config';

const app = createApp(App)
const pinia = createPinia()
app.use(PrimeVue);
app.component('BackButton', BackButton)
app.use(ConfirmationService);
app.use(pinia)
app.use(router)

pinia.use(piniaPluginPersistedState)

app.mount('#app')