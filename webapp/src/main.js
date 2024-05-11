import { createApp } from 'vue'

import App from './App.vue'
import Vue3ConfirmDialog from 'vue3-confirm-dialog';
import 'vue3-confirm-dialog/style';

// using ES6 modules
import mitt from 'mitt'


const app = createApp(App)
app.use(Vue3ConfirmDialog);
app.component('vue3-confirm-dialog', Vue3ConfirmDialog.default)
const emitter = mitt()
app.config.globalProperties.emitter = emitter
app.mount('#app')
