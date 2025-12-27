import assert from 'assert';
import { XY } from './infra/geom2d';


/**
 * The shape of a pentomino, defined by the coordinates of its 5 blocks
 * relative to an origin block at (0,0).
 * This is similar to the definition in `penta.py`, except that rotation
 * and flipping are around (0,0), where the Python version takes care
 * to preserve non-negative coordinates.
 * To recover the non-negative form, use `untranslate(topLeft())`.
 */
class Penta {
    constructor(public blocks: XY[]) {
        assert(blocks.length == 5)
    }

    translate([dx, dy]: XY) {
        return new Penta(this.blocks.map(([x, y]) => [x+dx, y+dy]));
    }

    untranslate([dx, dy]: XY) {
        return this.translate([-dx, -dy]);
    }

    flipx() {
        return new Penta(this.blocks.map(([x, y]) => [-x, y]));
    }

    transpose() {
        return new Penta(this.blocks.map(([x, y]) => [y, x]));
    }

    rot90cw() {
        return this.transpose().flipx();
    }

    topLeft() {
        return [Math.min(...this.blocks.map(([x, _]) => x)),
                Math.min(...this.blocks.map(([_, y]) => y))] as XY;
    }
}


export { Penta }