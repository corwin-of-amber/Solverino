<template>
    <Board :data="board" :size="[12, 5]"
        @cell:select="revealPiece($event.selection)"></Board>
    <div class="pieces">
        <div v-for="penta in pentas" class="card" 
                :class="{selected: selected.includes(penta)}"
                @click="toggleSelect(penta)">
            <Board :data="[[penta, [0,0]]]" selectMode="none"></Board>
        </div>
    </div>
    <button @click="solve">Solve</button>
</template>

<style lang="scss">
div.pieces {
    display: grid;
    grid-auto-flow: column;
    grid-auto-columns: max-content;
    gap: 5px;
    margin-top: 1em;

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

    solution: BoardData = []

    constructor() {
        super();
        this.pentas = []
    }

    async mounted() {
        await this.loadPentas();
        /** @todo load last set from local storage */
        this.selected = [2,5,10].map(i => this.pentas[i]);
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

    async solve() {
        let res = await fetch('http://localhost:2133/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({puzzle: this.selected})
        });
        let data = await res.json();
        if (data.status === 'success') {
            this.solution = (data.solution as {penta: Piece, at: XY}[]).map(
                ({penta, at}) => ([penta, at])
            );
            this.board = [];
        } else {
            alert('Error from server: ' + (data.error || 'Unknown error'));
        }
    }

    revealPiece(selection: {row: number, col: number}) {
        console.log('Revealing piece at', selection);
        this.board = 
            this.solution.filter(([{blocks}, [x, y]]) =>
                blocks.some(([dx, dy]) =>
                    x + dx == selection.col - 1 && y + dy == selection.row - 1));
    }
}


const MOCK_JSON = '[[[[1, 1], [0, 1], [2, 0], [1, 0], [0, 0]], [5, 0]], [[[2, 2], [2, 1], [0, 0], [1, 0], [2, 0]], [2, 0]], [[[0, 1], [1, 1], [2, 1], [3, 0], [3, 1]], [4, 3]], [[[2, 1], [2, 2], [1, 1], [0, 0], [0, 1]], [1, 0]], [[[0, 0], [0, 1], [0, 2], [1, 2], [0, 3]], [0, 0]], [[[2, 1], [2, 0], [1, 2], [1, 1], [0, 2]], [0, 2]], [[[0, 1], [1, 0], [1, 1], [2, 0], [3, 0]], [2, 3]], [[[0, 1], [1, 1], [1, 2], [2, 0], [2, 1]], [5, 1]]]';

export { IApp }
export default toNative(IApp)
</script>
