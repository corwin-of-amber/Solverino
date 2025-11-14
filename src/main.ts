import { createApp } from 'vue';
import App, { IApp } from './components/app.vue';

function main() {
    let app = createApp(App).mount('body') as IApp;
    Object.assign(window, { app });
}

document.addEventListener('DOMContentLoaded', main);