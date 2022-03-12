import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import naive from 'naive-ui'

createApp(App).use(naive).use(axios).mount('#app')
