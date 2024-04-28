import { createApp } from 'vue'
import App from './App.vue'
// using ES6 modules
import mitt from 'mitt'

const app = createApp(App)
const emitter = mitt()
app.config.globalProperties.emitter = emitter
app.mount('#app')
