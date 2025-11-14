import { createApp } from 'vue';
// @ts-ignore
import App, { IApp } from './components/app.vue';

function main() {
    let app = createApp(App) as IApp;
    app.board
    app.mount('body');
}

document.addEventListener('DOMContentLoaded', main);