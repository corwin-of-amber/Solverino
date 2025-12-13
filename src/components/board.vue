<template>
    <Grid :data="cells" :selectMode="selectMode"
          @select="$emit('cell:select', $event)"></Grid>
</template>

<style lang="scss">
div.tabular { gap: 0px; background: #ccc; }
.box {
    width: 35px;
    height: 35px;
}
.box:not(.vacant) { 
    --outer-border: 0.5px solid white; 
    --inner-border: 0.5px solid #fff4;

    border: var(--outer-border);
    &.adj-n { border-top: var(--inner-border); }
    &.adj-s { border-bottom: none; }
    &.adj-e { border-right: var(--inner-border); }
    &.adj-w { border-left: none; }
}

.box.vacant { border: 1px solid #00000022; }
</style>

<script lang="ts">
import _ from 'lodash';
import { Vue, toNative, Prop, Component } from 'vue-facing-decorator';

import { XY } from '../infra/geom2d';
import Grid from './grid';


@Component({
    emits: ['cell:select'],
    components: { Grid }
})
class IBoard extends Vue {
    @Prop size: XY
    @Prop data: BoardData = []
    @Prop setectMode: 'none' | 'single' | 'multiple' = 'none'

    get cells() {
        let board: {color: number, affin: string[]}[][] =
            this.size ? array2d(this.size) : [];

        for (let [{color, blocks}, [x, y]] of this.data) {
            for (let [dx, dy] of blocks) {
                (board[y + dy] ??= [])[x + dx] = {
                    color,
                    affin: this.affinity([dx, dy], blocks)
                };
            }
        }

        return board.map(row => 
            row.map(c => ({
                text: ' ',
                class: ['box', c?.color ? `color-${c?.color}` : 'vacant', 
                        ...c?.affin.map(a => `adj-${a}`) ?? []]
            }))
        );
    }

    affinity([x, y]: XY, l: XY[]) {
        return l.flatMap(([lx, ly]) =>
            (lx == x) ? {[-1]: ['n'], 1: ['s']}[ly - y]
          : (ly == y) ? {[-1]: ['w'], 1: ['e']}[lx - x] : undefined);
    }
}

type Piece = {color: number, blocks: XY[]};
type BoardData = [Piece, XY][];


function array2d<T>([szx, szy]: XY, fill: T = undefined): T[][] {
    return Array.from({length: szy}, () => 
               Array.from({length: szx}), () => fill);
}

function enumerate<T>(arr: T[]): [number, T][] {
    return arr.map((x, i) => [i, x]);
}


export { IBoard, BoardData, Piece }
export default toNative(IBoard)
</script>
