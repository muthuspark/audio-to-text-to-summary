// Import Vue.js
import { createApp } from 'vue';
import { createWebHashHistory, createRouter } from 'vue-router';

// Import main application component
import App from './App.vue';

import RecorderComponent from './components/RecorderComponent.vue';
import SummariesView from './pages/SummariesView.vue';

// Import confirm dialog component for Vue 3
import Vue3ConfirmDialog from 'vue3-confirm-dialog';
import 'vue3-confirm-dialog/style';

// Import event emitter for cross-component communication
import mitt from 'mitt';

// Define application routes
const routes = [
  { path: '/', component: RecorderComponent },
  { path: '/summary/:id', component: SummariesView, },
];

// Initialize router with memory history (for use in tests or non-browser environments)
const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

// Create a new Vue application instance
const app = createApp(App);

// Install Vue3ConfirmDialog plugin
app.use(Vue3ConfirmDialog);
// Install router
app.use(router);
// Register Vue3ConfirmDialog component globally
app.component('vue3-confirm-dialog', Vue3ConfirmDialog.default);

// Create a global event emitter and attach it to the application's config
const emitter = mitt();
app.config.globalProperties.emitter = emitter;

// Mount the Vue application to the DOM
app.mount('#app');
