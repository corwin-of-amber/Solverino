import { createApp } from 'vue';
import App, { IApp } from './components/app.vue';
import './index.scss';
import './colorset.scss';


function main() {
    let app = createApp(App).mount('#app') as IApp;
    Object.assign(window, { app });
}

document.addEventListener('DOMContentLoaded', main);