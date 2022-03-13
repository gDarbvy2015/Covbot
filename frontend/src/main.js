import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import naive from 'naive-ui'

createApp(App).use(naive).use(VueAxios, axios).mount('#app')
