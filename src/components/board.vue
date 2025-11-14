<template>
    <Grid :data="cells"></Grid>
</template>

<style lang="scss">
div.tabular { gap: 0px; background: #ccc; }
.box {
    width: 35px;
    height: 35px;
}
.box:not(.cell-empty) { border: 0.25px solid white; }
.box.cell-empty { border: 1px solid #00000022; }
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
        let board: number[][] = this.size ? array2d(this.size) : [];

        for (let [i, [blocks, [x, y]]] of enumerate(this.data)) {
            for (let [dx, dy] of blocks) {
                (board[y + dy] ??= [])[x + dx] = i + 1;
            }
        }

        return board.map(row => 
            row.map(c => ({text: ' ', class: ['box', `color-${c ?? 'empty'}`]})));
    }
}

type BoardData = [XY[], XY][];


function array2d<T>([szx, szy]: XY, fill: T = undefined): T[][] {
    return Array.from({length: szy}, () => 
               Array.from({length: szx}), () => fill);
}

function enumerate<T>(arr: T[]): [number, T][] {
    return arr.map((x, i) => [i, x]);
}


export { IBoard, BoardData }
export default toNative(IBoard)
</script>
