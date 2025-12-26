<template>
    <Board :data="board" :size="[12, 5]" ref="board"
        @pointerdown="pickBack"
        @cell:select="revealPiece($event.selection)"></Board>
    <div class="pieces" :class="{[`phase-${phase}`]: true}">
        <div v-for="penta in pentas" class="card" 
                :class="{selected: selected.includes(penta)}"
                @click="phase == 'select' && toggleSelect(penta)"
                @pointerdown="phase == 'game' && dragFromTray($event, penta)">
            <Board :data="[[penta, [0,0]]]" selectMode="none"></Board>
        </div>
    </div>
    <button @click="solve">Solve <em>🧠</em></button>
    <div class="switch-with-labels">
        <span>pick<em>🤏</em></span><slider-switch v-model="phaseSwitch"/><span><em>🤚</em> place</span>
    </div>

    <Draggable ref="dragged" class="drag-piece card" v-slot="{ position }"
            :prevent-default="true" :class="{hidden: !dragging.penta}"
            @end="dragEnd">
        <Board v-if="dragging.penta" :data="[[dragging.penta, [0,0]]]" selectMode="none"
            :style="dragStyle()"></Board>
        {{ (dragging.position = position) && undefined }}
    </Draggable>
</template>

<style lang="scss">
.drag-piece {
    position: fixed;
    pointer-events: none;
    &.hidden { display: none; }
    > div {
        transition: transform 0.1s ease-out;
    }
}
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
    }
}

div.pieces.phase-select {
    div.card.selected {
        top: -7px;
        outline: 1px solid #800;
        background-color: #fcda;
    }
}

div.pieces.phase-game {
    div.card:not(.selected) {
        opacity: 0.25;
        pointer-events: none;
    }
}

div.card {
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

div.switch-with-labels {
    display: inline-block;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    font-size: 75%;
    margin: 0 5px;
    label.switch { margin: 0 2px; }
}

em {
    display: inline-block;
    transform: scale(1.75);
    transform-origin: center;
    margin: 0 3px;
}
</style>

<script lang="ts">
import _ from 'lodash';
import { Vue, toNative, Component, Ref } from 'vue-facing-decorator';
import { UseDraggable } from '@vueuse/components';
import SliderSwitch from '../infra/components/slider-switch.vue';
import { XY } from '../infra/geom2d';
import Board, { BoardData, Piece } from './board.vue';
import { ITabular } from './grid';


@Component({
    components: { Board, SliderSwitch, Draggable: UseDraggable }
})
class IApp extends Vue {
    board: BoardData = []
    pentas: Piece[]

    selected: Piece[] = []

    solution: BoardData = []

    phaseSwitch: any = 1
    get phase() { return this.phaseSwitch ? 'game' : 'select'}

    constructor() {
        super();
        this.pentas = []
    }

    async mounted() {
        await this.loadPentas();
        /** @todo load last set from local storage */
        this.selected = [2,5,10].map(i => this.pentas[i]);

        document.addEventListener('keydown', ev => {
            switch (ev.code) {
                case 'ShiftLeft': 
                    this.dragging.rotate += 90; break;

            }
        });
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
        let xy = {x: selection.col - 1, y: selection.row - 1};

        this.board = 
            this.solution.filter(([{blocks}, [x, y]]) =>
                blocks.some(([dx, dy]) => x + dx == xy.x && y + dy == xy.y));
    }
    
    pickUpPiece(at: {row: number, col: number}) {
        let xy = [at.col - 1, at.row - 1],
            idx =
                this.board.findIndex(([{blocks}, [x, y]]) =>
                    blocks.some(([dx, dy]) => x + dx == xy[0] && y + dy == xy[1]));
        if (idx >= 0) {
            let [penta, [x, y]] = this.board[idx];
            this.board.splice(idx, 1);
            return [penta, [xy[0] - x, xy[1] - y]] as [Piece, XY];
        }
        else return undefined;
    }

    pickBack(ev: PointerEvent) {
        let c = ITabular.getCoordinates(ev.target as Element);

        let pick = this.pickUpPiece(c);
        if (pick) {
            let [penta, [dx, dy]] = pick;
            this.dragFromBoard(ev, penta, [dx, dy]);
        }
    }

    // -------------
    // Dragging Part
    // -------------

    @Ref dragged: {$el: HTMLElement}
    dragging: {
        penta?: Piece,
        grab?: {x: number, y: number},
        grabCell?: {row: number, col: number},
        position?: {x: number, y: number},
        scale: number,
        rotate: 0 | 90 | 180 | 270
    } = {scale: 3, rotate: 0}

    dragFromTray(ev: PointerEvent, penta: Piece) {
        this.dragging.penta = penta;
        let el = (ev.target as HTMLElement).closest('.tabular');
        let r = el.getBoundingClientRect();
        this.dragging.position.x = r.left;
        this.dragging.position.y = r.top;
        this.dragging.grab = {x: ev.clientX - r.left, y: ev.clientY - r.top};
        this.dragging.grabCell = ITabular.getCoordinates(ev.target as Element);;
        requestAnimationFrame(() => this.dragged.$el.dispatchEvent(ev));
        ev.preventDefault();
    }

    dragFromBoard(ev: PointerEvent, penta: Piece, [dx, dy]: XY) {
        this.dragging.penta = penta;
        this.dragging.grab = {x: dx * 12 + 6, y: dy * 12 + 6};
        this.dragging.position.x = ev.clientX - this.dragging.grab.x;
        this.dragging.position.y = ev.clientY - this.dragging.grab.y;
        this.dragging.grabCell = {row: dy + 1, col: dx + 1};
        requestAnimationFrame(() => this.dragged.$el.dispatchEvent(ev));
        ev.preventDefault();
    }

    dragRotate(by: 90 | -90) {
        let d = this.dragging.rotate + by;
        if (d > 360) d -= 360;
        if (d < 0) d += 360;
        this.dragging.rotate = d as 0 | 90 | 180 | 270;
    }

    dragStyle() {
        return {
            transform: `rotate(${this.dragging.rotate}deg) scale(${this.dragging.scale})`,
            'transform-origin': (pt => pt && `${pt.x}px ${pt.y}px`)(this.dragging.grab)
        };
    }

    dragEnd(pos: any, ev: DragEvent) {
        let coords = ITabular.getCoordinates(ev.target as Element);
        console.log('dropped at', coords);
        if (coords && this.dragging.grabCell) {
            this.board.push([this.dragging.penta, 
                [coords.col - this.dragging.grabCell.col, coords.row - this.dragging.grabCell.row]]);
        }
        this.dragging.penta = undefined;
    }

}


const MOCK_JSON = '[[[[1, 1], [0, 1], [2, 0], [1, 0], [0, 0]], [5, 0]], [[[2, 2], [2, 1], [0, 0], [1, 0], [2, 0]], [2, 0]], [[[0, 1], [1, 1], [2, 1], [3, 0], [3, 1]], [4, 3]], [[[2, 1], [2, 2], [1, 1], [0, 0], [0, 1]], [1, 0]], [[[0, 0], [0, 1], [0, 2], [1, 2], [0, 3]], [0, 0]], [[[2, 1], [2, 0], [1, 2], [1, 1], [0, 2]], [0, 2]], [[[0, 1], [1, 0], [1, 1], [2, 0], [3, 0]], [2, 3]], [[[0, 1], [1, 1], [1, 2], [2, 0], [2, 1]], [5, 1]]]';

export { IApp }
export default toNative(IApp)
</script>
