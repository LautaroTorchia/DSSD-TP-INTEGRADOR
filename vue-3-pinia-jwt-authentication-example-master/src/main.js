import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import { router } from './helpers'

import  BackButton  from '@/components/BackButton.vue'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.component('BackButton', BackButton)

app.mount('#app')
