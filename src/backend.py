
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)


sys.path += ['src/solver-py']


@app.route('/process', methods=['POST'])
def process():
    """Accept a JSON POST and return a JSON response.

    Expects Content-Type: application/json and a JSON object body.
    """
    if not request.is_json:
        return jsonify({'error': 'Request must be application/json'}), 400

    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({'error': 'JSON payload must be an object'}), 400

    solution = solve_katamino(data)
    if solution is None:
        return jsonify({'status': 'no solution'}), 200

    # Simple example processing: echo back the received JSON with a status
    return jsonify({'status': 'success', 'solution': solution}), 200


def solve_katamino(puzzle_json):
    from penta import Penta
    from solver import Solver

    pentas = [Penta(d['blocks']) for d in puzzle_json['puzzle']]
    colors = [d['color'] for d in puzzle_json['puzzle']]

    solver = Solver()
    solver.add_pentas(pentas)
    if solver.check():
        return [
            {'at': p.at, 'penta': {'blocks': p.penta.blocks, 'color': c}} 
            for p, c in zip(solver.solution(), colors)
        ]
    else:
        return None


if __name__ == '__main__':
    # For development only. In production use a WSGI server.
    app.run(host='0.0.0.0', port=2133)

# dev server with reload:
# python -m flask --app src/backend.py run -p 2133 --reload