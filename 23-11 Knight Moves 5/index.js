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

    sleep() {
        const matchingCells = [];
        const [currRow, currCol] = this.currentPosition;
        const currAlt = this._grid[currRow][currCol].altitude;

        for (let row of this._grid) {
            for (let cell of row) {
                if (cell.altitude.equals(currAlt)) {
                    matchingCells.push(cell);
                }
            }
        }

        const n = matchingCells.length;
        if (n == 0) {
            throw new Error(`Found no cells with altitude ${currAlt.toFraction()}`);
        }

        const sinkRate = math.fraction(1, n);
        for (let cell of matchingCells) {
            cell.altitude = cell.altitude.sub(sinkRate);
        }

        // Now elevate opposite
        const [oppRow, oppCol] = this.getOppositePosition(this.currentPosition);
        const oppCell = this._grid[oppRow][oppCol];
        oppCell.altitude = oppCell.altitude.add(sinkRate);

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



// // Initialise board
// // const buttons = [];
// for (let rowNum=0; rowNum < HEIGHT; rowNum++) {
//     // buttons.push([]);
//     for (let colNum=0; colNum < WIDTH; colNum++) {
//         const fraction = math.fraction(board[rowNum][colNum]);
//         setAltitude([rowNum, colNum], fraction)
//         setButtonPosition([rowNum, colNum])
//         // buttons[buttons.length - 1].push(button);
//     }
// }

// function setAltitude(position, fraction) {
//     const button = positionToButton(position);

//     button.dataset.fractionN = fraction.n;
//     button.dataset.fractionD = fraction.d;
//     button.dataset.fractionS = fraction.s;
//     button.innerText = fraction.toFraction(true);
// }

// function setButtonPosition(position) {
//     const button = positionToButton(position);
//     const [row, col] = position;
//     button.dataset.row = row;
//     button.dataset.col = col;
// }

// function moveTo(newPosition) {
//     currentPosition = newPosition;
//     const button = positionToButton(currentPosition);
//     button.dataset.current = true;
//     checkState();
// }

// function getAltitude(position) {
//     const button = positionToButton(position);

//     let n = parseInt(button.dataset.fractionN);
//     let d = parseInt(button.dataset.fractionD);
//     let s = parseInt(button.dataset.fractionS);

//     let altitude = math.fraction(n, d);
//     if (s == '-1') {
//         altitude = altitude.mul(-1);
//     }

//     return altitude;
// }


// checkState();



// function positionToButton(position) {
//     const [rowNum, colNum] = position;
//     const rows = document.querySelectorAll("div.row");
//     const row = rows[rowNum];
//     const cols = row.querySelectorAll("button");
//     return cols[colNum];
// }

// function positionTo1DIndex(position) {
//     const [row, col] = position;
//     return row * WIDTH + col;
// }


// function highlightCurrentPosition(position) {
//     const button = positionToButton(position);
//     button.dataset.current = true;
// }

// function getOppositePosition(position) {
//     const [row, col] = position;
//     const oppRow = HEIGHT - row - 1;
//     const oppCol = WIDTH - col - 1;
//     return [oppRow, oppCol];
// }

// function getAllButtons() {
//     const buttons = [];
//     for (let rowNum=0; rowNum<HEIGHT; rowNum++) {
//         for (let colNum=0; colNum<WIDTH; colNum++) {
//             let button = positionToButton([rowNum, colNum]);
//             buttons.push(button);
//         }
//     }
    
//     return buttons;
// }

// function clearStates() {
//     const buttons = getAllButtons();
//     for (let button of buttons) {
//         button.dataset.reachable = false;
//         button.dataset.current = false;
//         button.onclick = null;
//     }
// }

// function sleepBoard() {
//     const buttons = getAllButtons();
//     const currentButton = buttons[positionTo1DIndex(currentPosition)];
//     const currentAltitude = getAltitude(currentPosition);
//     const oppPosition = getOppositePosition(currentPosition)
//     // const currentAltitude = parseFloat(currentButton.innerText);
    
//     let matchingPositions = [];
//     let oppositeDidMatch = false;
//     for (let rowNum=0; rowNum<HEIGHT; rowNum++) {
//         for (let colNum=0; colNum<WIDTH; colNum++) {
//             const position = [rowNum, colNum]
//             const altitudeMatch = currentAltitude.equals(getAltitude(position));
//             const isOpposite = arrayEquals(position, oppPosition);
//             if (altitudeMatch && !isOpposite) {
//                 if (isOpposite) {
//                     oppositeDidMatch = true;
//                 } else {
//                     matchingPositions.push(position);
//                 }
//             }
//         }
//     }
//     console.log(matchingPositions);

//     const n = matchingPositions.length;
//     // Should never happen since button should always match itself!
//     if (n == 0) {
//         throw new Error(`Found no button matching altitude '${currentAltitude}' from position ${currentPosition}`);
//     }
//     const sinkRate = math.fraction(1, n);

//     // Sink all cells with same altitude
//     for (let position of matchingPositions) {
//         const currAlt = getAltitude(position);
//         const newAlt = currAlt.sub(sinkRate);
//         setAltitude(position, newAlt)
//     }

//     // Rise diametrically opposite cell (if it wasn't same altitude)
//     if (!oppositeDidMatch) {
//         const currAlt = getAltitude(oppPosition);
//         const newAlt = currAlt.add(sinkRate);
//         setAltitude(oppPosition, newAlt);
//     }

//     incrementTime();
//     checkState();
// }

// function checkState() {
//     clearStates();
//     highlightCurrentPosition(currentPosition);
    
//     const currentAlt = getAltitude(currentPosition);
//     const [row, col] = currentPosition;
    
//     // Find all reachable cells
//     let reachableButtons = [];

//     const validCombos = [[0, 1, 2], [0, 1, -2], [0, -1, 2], [0, -1, -2]];
//     for (let combo of validCombos) {
//         for (let perm of permutator(combo)) {
//             const [rowDiff, colDiff, altDiff] = perm;
//             const newRow = row + rowDiff;
//             const newCol = col + colDiff;
//             if (newRow < 0 || newRow >= HEIGHT || newCol < 0 || newCol >= WIDTH) {
//                 continue;
//             }

//             const newAlt = currentAlt + altDiff;
//             if (getAltitude([newRow, newCol]) == newAlt) {
//                 reachableButtons.push(positionToButton([newRow, newCol]));
//             }
//         }
//     }

//     highlightReachable(reachableButtons);

//     return reachableButtons;
// }

// function incrementTime() {
//     const span = document.querySelector("#time");
//     let newTime = parseInt(span.innerText) + 1;
//     span.innerText = newTime.toString();
// }

// function highlightReachable(buttons) {
//     for (let button of buttons) {
//         button.dataset.reachable = true;
//         button.onclick = () => {
//             console.log("CLICKED!");
//             moveTo([button.dataset.row, button.dataset.col]);
//         };
//     }
// }


// /**
//  * Generate all combinations of an array. Taken from https://stackoverflow.com/a/61418166
//  * @param {Array} sourceArray - Array of input elements.
//  * @param {number} comboLength - Desired length of combinations.
//  * @return {Array} Array of combination arrays.
//  */
// function generateCombinations(sourceArray, comboLength) {
//     const sourceLength = sourceArray.length;
//     if (comboLength > sourceLength) return [];
  
//     const combos = []; // Stores valid combinations as they are generated.
  
//     // Accepts a partial combination, an index into sourceArray, 
//     // and the number of elements required to be added to create a full-length combination.
//     // Called recursively to build combinations, adding subsequent elements at each call depth.
//     const makeNextCombos = (workingCombo, currentIndex, remainingCount) => {
//       const oneAwayFromComboLength = remainingCount == 1;
  
//       // For each element that remaines to be added to the working combination.
//       for (let sourceIndex = currentIndex; sourceIndex < sourceLength; sourceIndex++) {
//         // Get next (possibly partial) combination.
//         const next = [ ...workingCombo, sourceArray[sourceIndex] ];
  
//         if (oneAwayFromComboLength) {
//           // Combo of right length found, save it.
//           combos.push(next);
//         }
//         else {
//           // Otherwise go deeper to add more elements to the current partial combination.
//           makeNextCombos(next, sourceIndex + 1, remainingCount - 1);
//         }
//           }
//     }
  
//     makeNextCombos([], 0, comboLength);
//     return combos;
// }
  

// // Taken from https://stackoverflow.com/a/20871714
// function permutator(inputArr) {
//     let result = [];

//     const permute = (arr, m = []) => {
//         if (arr.length === 0) {
//         result.push(m)
//         } else {
//         for (let i = 0; i < arr.length; i++) {
//             let curr = arr.slice();
//             let next = curr.splice(i, 1);
//             permute(curr.slice(), m.concat(next))
//         }
//         }
//     }

//     permute(inputArr)

//     return result;
// }

// // Taken from https://flexiple.com/javascript/javascript-array-equality
// // Why is this not built in to JS?
// function arrayEquals(a, b) {
//     return Array.isArray(a) &&
//         Array.isArray(b) &&
//         a.length === b.length &&
//         a.every((val, index) => val === b[index]);
// }