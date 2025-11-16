<template>
    <Board :data="board" :size="[12, 5]"></Board>
    <div class="pieces">
        <div v-for="penta in pentas" class="card" 
                :class="{selected: selected.includes(penta)}"
                @click="toggleSelect(penta)">
            <Board :data="[[penta, [0,0]]]" selectMode="none"></Board>
        </div>
    </div>
</template>

<style lang="scss">
div.pieces {
    display: grid;
    grid-auto-flow: column;
    grid-auto-columns: max-content;
    gap: 5px;

    div.card {
        display: flex;
        align-items: center;
        height: 100%;    
        padding: 5px;    
        border-radius: 5px;
        position: relative;
        transition: top 0.25s ease-out,
                    background-color 0.25s ease-in,
                    outline-color 0.5s;
        top: 0px;
        outline: 1px solid transparent;
        &.selected {
            top: -7px;
            outline: 1px solid #800;
            background-color: #fcda;
        }
    }

    .tabular {
        background: none;
        filter: drop-shadow(0px 0px 2px #0006);
        .box {
            height: 12px;
            width: 12px;
            --outer-border: 1px solid #3334;
            --inner-border: 0.5px solid #fff6;
        }
    }
}

</style>

<script lang="ts">
import _ from 'lodash';
import { Vue, toNative, Component } from 'vue-facing-decorator';
import { XY } from '../infra/geom2d';
import Board, { BoardData, Piece } from './board.vue';


@Component({
    components: { Board }
})
class IApp extends Vue {
    board: BoardData = (JSON.parse(MOCK_JSON) as [XY[], XY][]).map(
            ([blocks, at], i) => ([{color: i + 1, blocks}, at])
        );
    pentas: Piece[]

    selected: Piece[] = []

    constructor() {
        super();
        this.pentas = []
    }

    mounted() {
        this.loadPentas();
    }

    async loadPentas() {
        this.pentas = (await (await fetch('/data/pentas.json')).json() as XY[][]).map(
            (blocks: XY[], i) => ({color: i + 1, blocks})
        );
    }

    get pentasData() {
        return this.pentas.slice(0, 3).map((shape, i) => [shape, [0,0]]);
    }

    toggleSelect(penta: Piece) {
        if (this.selected.includes(penta)) {
            _.remove(this.selected, p => p === penta);
        } else {
            this.selected.push(penta);
        }
    }
}

const MOCK_JSON = '[[[[1, 1], [0, 1], [2, 0], [1, 0], [0, 0]], [5, 0]], [[[2, 2], [2, 1], [0, 0], [1, 0], [2, 0]], [2, 0]], [[[0, 1], [1, 1], [2, 1], [3, 0], [3, 1]], [4, 3]], [[[2, 1], [2, 2], [1, 1], [0, 0], [0, 1]], [1, 0]], [[[0, 0], [0, 1], [0, 2], [1, 2], [0, 3]], [0, 0]], [[[2, 1], [2, 0], [1, 2], [1, 1], [0, 2]], [0, 2]], [[[0, 1], [1, 0], [1, 1], [2, 0], [3, 0]], [2, 3]], [[[0, 1], [1, 1], [1, 2], [2, 0], [2, 1]], [5, 1]]]';

export { IApp }
export default toNative(IApp)
</script>
