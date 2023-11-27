"use strict";


function createRowElement(rowNum) {
    const rowDiv = document.createElement("div");
    rowDiv.classList.add("row");
    rowDiv.dataset.row = rowNum;
    return rowDiv;
}

function createCellElement(row, colNum, altitude) {
    const cellEl = document.createElement("button");
}


class Board {
    constructor(altitudes, currentPosition) {
        this._height = altitudes.length;
        this._width = altitudes[0].length;
        this.initBoard(altitudes);

        this.currentPosition = currentPosition;
    }

    get element() {
        return document.querySelector(".board");
    }

    initBoard(altitudes) {
        this._grid = [];
        this.element.innerHTML = "";
        for (let rowNum = 0; rowNum < this._height; rowNum++) {
            this._grid[rowNum] = [];
            
            this.element.appendChild(createRowElement(rowNum));
            for (let colNum = 0; colNum < this._width; colNum++) {
                // Make actual board element
                
                this._grid[rowNum][colNum] = new Cell(rowNum, colNum, altitudes[rowNum][colNum]);
            }
        }   
    }
    
    allowedMoves() {
        const allowedCombos = [
            [0, 1, 2], [0, -1, 2],
            [0, 2, 1], [0, -2, 1],
            [1, 0, 2], [1, 2, 0], [1, -2, 0],
            [2, 0, 1], [2, 1, 0], [2, -1, 0],
            [-1, 0, 2], [-1, 2, 0], [-1, -2, 0],
            [-2, 0, 1], [-2, 1, 0], [-2, -1, 0],
        ];

        const [currRow, currCol] = this.currentPosition;
        const currAlt = this._grid[currRow][currCol].altitude;
        const allowedMoves = [];
        for (let combo of allowedCombos) {
            const [rowDiff, colDiff, targetAltDiff] = combo;

            const targetRow = currRow + rowDiff;
            const targetCol = currCol + colDiff;
            // Check if out of bounds
            if (targetRow < 0 || targetRow >= this._height || targetCol < 0 || targetCol >= this._width) {
                continue;
            }

            // const desiredAlt = this._grid[currRow][currCol].altitude.add(altDiff);
            const targetCell = this._grid[targetRow][targetCol];
            const actualAltDiff = targetCell.altitude.sub(currAlt).abs();
            if (actualAltDiff.equals(targetAltDiff)) {
                allowedMoves.push(combo);
                console.log(`Making ${targetCell._button} clickable!`);
                targetCell.makeReachable(() => {
                    console.log("CLICKED!");
                    this.moveTo([targetRow, targetCol]);
                });
                console.log(`Clickable? ${targetCell._button.onclick}`);
                console.log(`Made ${targetCell._button} clickable!`);
            } else {
                targetCell.makeUnreachable();
                console.log(`Combo=${combo}; targetAlt=${targetCell.altitude.toFraction()}; currAlt=${currAlt.toFraction()}`)
                // console.log(`Combo=${combo}; desiredAlt=${desiredAlt.toFraction()}; actualAlt=${this._grid[targetRow][targetCol].altitude.toFraction()}; targetPos=(${targetRow}, ${targetCol})`);
            }
        }

        for (let row of this._grid) {
            for (let cell of row) {
                console.log(`2. Clickable? ${cell._button.onclick}`);
            }
        }

        return allowedMoves;
    }

    moveTo(newPosition) {
        this.currentPosition = newPosition;
    }

    getOppositePosition(position) {
        const row = this._height - position[0] - 1;
        const col = this._width - position[1] - 1;
        return [row, col];
    }

    /**
     * Returns list of cells with same height as that of given position, as well
     * as whether the opposite cell matched altitude. Note that the opposite cell
     * will _never_ be returned in the list since this method is intended to find
     * cells that _sink_.
     * 
     * @param {*} position Position to compare heights with
     */
    findMatchingHeights(position) {
        const [currRow, currCol] = position;
        const currAlt = this._grid[currRow][currCol].altitude;
        const [oppRow, oppCol] = this.getOppositePosition(position);
        
        const matchingCells = [];0
        let oppositeMatched = false;
        for (let row of this._grid) {
            for (let cell of row) {
                if (cell.altitude.equals(currAlt)) {
                    if (cell.row == oppRow && cell.col == oppCol) {
                        oppositeMatched = true;
                    } else {
                        matchingCells.push(cell);
                    }
                }
            }
        }

        return {
            "matchingCells": matchingCells,
            "oppositeMatched": oppositeMatched
        };
    }

    sleep() {
        const {matchingCells, oppositeMatched} = this.findMatchingHeights(this.currentPosition);
        console.log(matchingCells);
        console.log(oppositeMatched);
        const n = matchingCells.length;
        const sinkRate = math.fraction(1, n);
        
        // Sink all non-opposite cells with same altitude
        for (let cell of matchingCells) {
            cell.altitude = cell.altitude.sub(sinkRate);
        }

        // Elevate opposite cell unless it was same altitude
        if (!oppositeMatched) {
            const [oppRow, oppCol] = this.getOppositePosition(this.currentPosition);
            const oppCell = this._grid[oppRow][oppCol];
            oppCell.altitude = oppCell.altitude.add(sinkRate);
        }

        this.clearReachable();
        this.allowedMoves();
        incrementTime();
    }

    get currentPosition() {
        return this._currentPosition;
    }

    clearReachable() {
        for (let otherRow of this._grid) {
            for (let cell of otherRow) {
                cell.makeUnreachable();
            }
        }
    }

    set currentPosition(position) {
        console.log("Setting positio...");
        // Clear previous position
        if (this._currentPosition !== undefined) {
            const [prevRow, prevCol] = this._currentPosition;
            this._grid[prevRow][prevCol].unselect();
        }

        this.clearReachable();

        // Set new position
        this._currentPosition = position;
        const [row, col] = position;
        this._grid[row][col].select();
        this._grid[row][col].makeUnreachable();

        console.log("Set position!");
        this.allowedMoves();
    } 
}


class Cell {
    constructor(row, col, altitude) {
        this.row = row;
        this.col = col;
        this.isSelected = false;
        this.isReachable = false;
        this._button = this.createElement();

        this.altitude = math.fraction(altitude);
    }

    createElement() {
        const row = document.querySelector(`.row[data-row="${this.row}"]`);
        const button = document.createElement("button");
        button.classList.add("cell");
        button.dataset.row = this.row;
        button.dataset.col = this.col;
        row.appendChild(button);
        return button;
    }

    clearState() {
        this.isSelected = false;
        this.isReachable = false;
    }

    select() {
        this.isSelected = true;
        this._button.classList.add("selected");
    }

    unselect() {
        this.isSelected = false;
        this._button.classList.remove("selected");
    }

    makeReachable(callback) {
        console.log("HERE!");
        this.isReachable = true;
        this._button.classList.add("reachable");
        this._button.onclick = callback;
        this._button.disabled = null;
        console.log(callback);
        console.log(this._button);
        console.log(this._button.classList);
    }

    makeUnreachable() {
        this.isReachable = false;
        this._button.classList.remove("reachable");
        this._button.onclick = null;
        this._button.disabled = true;
    }

    get altitude() {
        const n = parseInt(this._button.dataset.fracN);
        const d = parseInt(this._button.dataset.fracD);
        const s = this._button.dataset.fracS;
        
        let altitude = math.fraction(n, d);
        if (s == "-1") {
            altitude = altitude.mul(-1);
        }
        return altitude;
    }

    set altitude(val) {
        val = math.fraction(val);

        this._altitude = val;
        this._button.dataset.fracN = val.n;
        this._button.dataset.fracD = val.d;
        this._button.dataset.fracS = val.s;
        this._button.innerText = val.toFraction(true);
    }
}

function incrementTime() {
    const span = document.querySelector("#time");
    let newTime = parseInt(span.innerText) + 1;
    span.innerText = newTime.toString();
}


const board = new Board([
    [11, 10, 11, 14],
    [8, 6, 9, 9],
    [10, 4, 3, 1],
    [7, 6, 5, 0]],
    [3, 0]
    );
document.querySelector(".sleep").onclick = () => board.sleep();