const boardContainer = document.getElementById('board');
const statusLabel = document.getElementById('status');
const difficultyMenu = document.getElementById('difficulty');
const resetBtn = document.getElementById('reset-btn');

let lockInteraction = false;

function buildBoard() {
    boardContainer.innerHTML = '';
    // Build from Row index 5 down to 0 so indexing works perfectly matching the Flask array matrix
    for (let r = 5; r >= 0; r--) {
        for (let c = 0; c < 7; c++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.id = `cell-${r}-${c}`;
            cell.addEventListener('click', () => dispatchMove(c));
            boardContainer.appendChild(cell);
        }
    }
}

function refreshUI(matrix) {
    for (let r = 0; r < 6; r++) {
        for (let c = 0; c < 7; c++) {
            const cell = document.getElementById(`cell-${r}-${c}`);
            cell.className = 'cell'; 
            if (matrix[r][c] === 1) cell.classList.add('player-human');
            if (matrix[r][c] === 2) cell.classList.add('player-ai');
        }
    }
}

async function dispatchMove(col) {
    if (lockInteraction) return;
    lockInteraction = true;
    statusLabel.innerText = "AI computing optimal branch countermove...";

    const packet = await fetch('/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ column: col, difficulty: difficultyMenu.value })
    });

    if (packet.status === 400) {
        statusLabel.innerText = "Column is packed! Choose a different spot.";
        lockInteraction = false;
        return;
    }

    const report = await packet.json();
    refreshUI(report.board);

    if (report.status === 'win') {
        statusLabel.innerText = `${report.winner} Wins the match! 🏆`;
    } else if (report.status === 'draw') {
        statusLabel.innerText = "Draw match! No open legal nodes remaining.";
    } else {
        statusLabel.innerText = "Your Turn! Pick another column.";
        lockInteraction = false;
    }
}

resetBtn.addEventListener('click', async () => {
    const packet = await fetch('/reset', { method: 'POST' });
    const data = await packet.json();
    refreshUI(data.board);
    statusLabel.innerText = "Board reset! Place your opening chip.";
    lockInteraction = false;
});

buildBoard();
