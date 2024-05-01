import { createApp } from 'vue'
import App from './App.vue'
import '@picocss/pico/css/pico.min.css';
// using ES6 modules
import mitt from 'mitt'

const app = createApp(App)
const emitter = mitt()
app.config.globalProperties.emitter = emitter
app.mount('#app')
