import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import naive from 'naive-ui'
import store from './store'

createApp(App).use(store).use(naive).use(VueAxios, axios).mount('#app')
