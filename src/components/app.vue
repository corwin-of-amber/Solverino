<template>
    <Grid :data="boardCells"></Grid>
</template>

<style lang="scss">
* { box-sizing: border-box; }
div.tabular { gap: 0px; background: #ccc; }
.box {
    width: 35px;
    height: 35px;
}
.box.cell-0 { border: 1px solid #00000022; }
.box.cell-1 { background: #d61b1b; }
.box.cell-2 { background: #2222d9ff; }
.box.cell-3 { background: #1f801fff; }
.box.cell-4 { background: #fcfc12ff; }
.box.cell-5 { background: #b30fb3ff; }
.box.cell-6 { background: #54d3d3ff; }
.box.cell-7 { background: #8665ffff; }
.box.cell-8 { background: #ff61daff; }
</style>

<script lang="ts">
import _ from 'lodash';
import { Vue, toNative, Ref, Prop, Component } from 'vue-facing-decorator';
import Grid from './grid';

@Component({
    components: { Grid }
})
class IApp extends Vue {
    board: number[][] = []

    constructor() {
        super();

        this.board = Array.from({length: 5},
            () => Array.from({length: 12}, () => 0));

        for (let [[blocks, at], i] of MOCK_DATA.map((x, i) => [x, i])) {
            for (let [x, y] of blocks) {
                this.board[y + at[1]][x + at[0]] = i + 1;
            }
        }
    }

    get boardCells() {
        return this.board
        .map(row => row.map(cell => ({text: ' ', class: ['box', 'cell-' + cell]})));
    }
}

const MOCK_JSON = '[[[[1, 1], [0, 1], [2, 0], [1, 0], [0, 0]], [5, 0]], [[[2, 2], [2, 1], [0, 0], [1, 0], [2, 0]], [2, 0]], [[[0, 1], [1, 1], [2, 1], [3, 0], [3, 1]], [4, 3]], [[[2, 1], [2, 2], [1, 1], [0, 0], [0, 1]], [1, 0]], [[[0, 0], [0, 1], [0, 2], [1, 2], [0, 3]], [0, 0]], [[[2, 1], [2, 0], [1, 2], [1, 1], [0, 2]], [0, 2]], [[[0, 1], [1, 0], [1, 1], [2, 0], [3, 0]], [2, 3]], [[[0, 1], [1, 1], [1, 2], [2, 0], [2, 1]], [5, 1]]]',
        MOCK_DATA = JSON.parse(MOCK_JSON);

export { IApp }
export default toNative(IApp)
</script>
