<template>
    <Grid :data="cells"></Grid>
</template>

<style lang="scss">
* { box-sizing: border-box; }
div.tabular { gap: 0px; background: #ccc; }
.box {
    width: 35px;
    height: 35px;
}
.box.cell-empty { border: 1px solid #00000022; }
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
import { Vue, toNative, Prop, Component } from 'vue-facing-decorator';

import { XY } from '../infra/geom2d';
import Grid from './grid';


@Component({
    components: { Grid }
})
class IBoard extends Vue {
    @Prop size: XY
    @Prop data: BoardData = []

    get cells() {
        /** @todo default width should be auto calc-ed */
        let [szx, szy] = this.size ?? [];
        let board = this.size ? Array.from({length: szy},
            () => Array.from({length: szx}), () => undefined) : [];

        for (let [i, [blocks, [x, y]]] of enumerate(this.data)) {
            for (let [dx, dy] of blocks) {
                (board[y + dy] ??= [])[x + dx] = i + 1;
            }
        }

        console.log(board.map(row => 
            row.map(c => ({text: ' ', class: ['box', `cell-${c ?? 'empty'}`]}))));

        return board.map(row => 
            row.map(c => ({text: ' ', class: ['box', `cell-${c ?? 'empty'}`]})));
    }
}

type BoardData = [XY[], XY][];


function enumerate<T>(arr: T[]): [number, T][] {
    return arr.map((x, i) => [i, x]);
}

export { IBoard, BoardData }
export default toNative(IBoard)
</script>
