document.addEventListener('DOMContentLoaded', () => {
    const board = document.getElementById('board');
    const rows = 10;
    const cols = 17;

    const grid = Array.from({ length: rows }, () =>
        Array.from({ length: cols }, () => Math.floor(Math.random() * 9) + 1)
    );

    function renderGrid() {
        board.innerHTML = '';
        grid.forEach((row, i) => {
            row.forEach((value, j) => {
                const cell = document.createElement('div');
                cell.classList.add('cell');
                cell.textContent = value === 0 ? '' : value;
                cell.dataset.row = i;
                cell.dataset.col = j;
                board.appendChild(cell);
            });
        });
    }

    renderGrid();

    let isDragging = false;
    let startCell = null;
    let selectedCells = [];

    function getCellsInRectangle(startRow, startCol, endRow, endCol) {
        const cells = [];
        const minRow = Math.min(startRow, endRow);
        const maxRow = Math.max(startRow, endRow);
        const minCol = Math.min(startCol, endCol);
        const maxCol = Math.max(startCol, endCol);

        for (let i = minRow; i <= maxRow; i++) {
            for (let j = minCol; j <= maxCol; j++) {
                cells.push({ row: i, col: j });
            }
        }
        return cells;
    }

    function highlightCells(cells) {
        selectedCells.forEach(cell => {
            const cellElement = document.querySelector(`.cell[data-row="${cell.row}"][data-col="${cell.col}"]`);
            cellElement.classList.remove('selected');
        });
        selectedCells = cells;
        cells.forEach(cell => {
            const cellElement = document.querySelector(`.cell[data-row="${cell.row}"][data-col="${cell.col}"]`);
            cellElement.classList.add('selected');
        });
    }

    function checkSum(cells) {
        const sum = cells.reduce((acc, cell) => acc + grid[cell.row][cell.col], 0);
        return sum === 10;
    }

    function clearSelectedCells(cells) {
        cells.forEach(cell => {
            grid[cell.row][cell.col] = 0;
        });
        renderGrid();
    }

    board.addEventListener('mousedown', (e) => {
        if (e.target.classList.contains('cell')) {
            isDragging = true;
            const row = parseInt(e.target.dataset.row);
            const col = parseInt(e.target.dataset.col);
            startCell = { row, col };
            selectedCells = [{ row, col }];
            highlightCells(selectedCells);
        }
    });

    board.addEventListener('mousemove', (e) => {
        if (isDragging && e.target.classList.contains('cell')) {
            const endRow = parseInt(e.target.dataset.row);
            const endCol = parseInt(e.target.dataset.col);
            const cells = getCellsInRectangle(startCell.row, startCell.col, endRow, endCol);
            highlightCells(cells);
        }
    });

    board.addEventListener('mouseup', () => {
        if (isDragging) {
            isDragging = false;
            if (checkSum(selectedCells)) {
                clearSelectedCells(selectedCells);
            } else {
                highlightCells([]);
            }
        }
    });
});