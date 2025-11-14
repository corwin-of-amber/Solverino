<template>
    <Board :data="board" :size="[12, 5]"></Board>
    <div class="pieces">
        <Board v-for="penta in pentas" :data="[[penta, [0,0]]]"></Board>
    </div>
</template>

<style lang="scss">
div.pieces {
    display: grid;
    grid-auto-flow: column;
    grid-auto-columns: max-content;
    gap: 5px;
    .tabular {
        background: none;
    }
    .box {
        height: 10px;
        width: 10px;
    }
}

</style>

<script lang="ts">
import _ from 'lodash';
import { Vue, toNative, Component } from 'vue-facing-decorator';
import { XY } from '../infra/geom2d';
import Board, { BoardData } from './board.vue';


@Component({
    components: { Board }
})
class IApp extends Vue {
    board: BoardData = JSON.parse(MOCK_JSON)
    pentas: XY[][]

    constructor() {
        super();
        this.pentas = []
    }

    mounted() {
        this.loadPentas();
    }

    async loadPentas() {
        this.pentas = await (await fetch('/data/pentas.json')).json();
    }

    get pentasData() {
        return this.pentas.slice(0, 3).map((shape, i) => [shape, [0,0]]);
    }
}

const MOCK_JSON = '[[[[1, 1], [0, 1], [2, 0], [1, 0], [0, 0]], [5, 0]], [[[2, 2], [2, 1], [0, 0], [1, 0], [2, 0]], [2, 0]], [[[0, 1], [1, 1], [2, 1], [3, 0], [3, 1]], [4, 3]], [[[2, 1], [2, 2], [1, 1], [0, 0], [0, 1]], [1, 0]], [[[0, 0], [0, 1], [0, 2], [1, 2], [0, 3]], [0, 0]], [[[2, 1], [2, 0], [1, 2], [1, 1], [0, 2]], [0, 2]], [[[0, 1], [1, 0], [1, 1], [2, 0], [3, 0]], [2, 3]], [[[0, 1], [1, 1], [1, 2], [2, 0], [2, 1]], [5, 1]]]';

export { IApp }
export default toNative(IApp)
</script>
