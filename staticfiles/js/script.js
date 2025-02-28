
document.addEventListener("DOMContentLoaded", function () {
    let selectedCell = null;
    let selectedCellId = "";
    Object.keys(savedCells).forEach(cellId => {
        let cell = document.getElementById(cellId);
        if (cell) {
            cell.innerText = savedCells[cellId];  // ✅ Restore saved value
        }
    });


    window.selectCell = function(row, col) {
        if (selectedCell) {
            selectedCell.classList.remove("selected");
        }
        selectedCellId = `cell-${row}-${col}`;
        selectedCell = document.getElementById(selectedCellId);
        selectedCell.classList.add("selected");
        document.getElementById("formula-bar").value = selectedCell.innerText;
    };

    window.restoreSelection = function () {
        if (selectedCell) {
            selectedCell.classList.add("selected");
        }
    };

    window.applyFormula = function (event){
        if (event.key === 'Enter' && selectedCell) {
            let formula = document.getElementById("formula-bar").value;
            if (formula.startsWith("=")) {
                selectedCell.innerText = evaluateFormula(formula.substring(1));
            } else {
                selectedCell.innerText = formula;
            }
            event.preventDefault();
        }
    }

    window.getCellValue=function(cellId) {
        let cell = document.getElementById(cellId);
        return cell ? parseFloat(cell.innerText) || 0 : 0;
    };

    window.evaluateFormula=function(expression) {
        if (expression.match(/^SUM\((.*?)\)$/i)) {
            return sumFunction(expression);
        } else if (expression.match(/^AVERAGE\((.*?)\)$/i)) {
            return averageFunction(expression);
        } else if (expression.match(/^MAX\((.*?)\)$/i)) {
            return maxFunction(expression);
        } else if (expression.match(/^MIN\((.*?)\)$/i)) {
            return minFunction(expression);
        } else if (expression.match(/^COUNT\((.*?)\)$/i)) {
            return countFunction(expression);
        }
        return "ERROR";
    };

    window.sumFunction=function(expression) {
        let range = expression.match(/\((.*?)\)/)[1];
        let values = parseRange(range);
        return values.reduce((a, b) => a + b, 0);
    };

    window.averageFunction=function(expression) {
        let range = expression.match(/\((.*?)\)/)[1];
        let values = parseRange(range);
        return values.length ? (values.reduce((a, b) => a + b, 0) / values.length) : 0;
    };

    window.maxFunction=function(expression) {
        let range = expression.match(/\((.*?)\)/)[1];
        let values = parseRange(range);
        return Math.max(...values);
    };

    window.minFunction=function(expression) {
        let range = expression.match(/\((.*?)\)/)[1];
        let values = parseRange(range);
        return Math.min(...values);
    };

    window.countFunction=function(expression) {
        let range = expression.match(/\((.*?)\)/)[1];
        let values = parseRange(range);
        return values.length;
    };

    window.parseRange= function(range) {
        let [start, end] = range.split(":"), values = [];
        let startCell = start.match(/([A-Z]+)(\d+)/), endCell = end.match(/([A-Z]+)(\d+)/);
        
        if (!startCell || !endCell) return [];
        let startRow = parseInt(startCell[2]), endRow = parseInt(endCell[2]);
        let col = startCell[1];
        
        for (let i = startRow; i <= endRow; i++) {
            values.push(getCellValue(`cell-${i}-${col.charCodeAt(0) - 65 + 1}`));
        }
        return values;
    };


    window.addRow = function () {
        let table = document.getElementById("spreadsheet").getElementsByTagName('tbody')[0];
        let rowCount = table.rows.length + 1;
        let newRow = table.insertRow();
        let headerCell = newRow.insertCell(0);
        headerCell.outerHTML = `<th class="row-header">${rowCount}</th>`;
        for (let i = 1; i <= table.rows[0].cells.length - 1; i++) {
            let cell = newRow.insertCell(i);
            cell.contentEditable = "true";
            cell.id = `cell-${rowCount}-${i}`;
        }
    };

    window.addColumn = function () {
        let table = document.getElementById("spreadsheet");
        let colCount = table.rows[0].cells.length;
        let headerRow = table.rows[0];
        let newHeader = headerRow.insertCell(colCount);
        newHeader.outerHTML = `<th>${String.fromCharCode(64 + colCount)}</th>`;
        
        for (let i = 1; i < table.rows.length; i++) {
            let row = table.rows[i];
            let cell = row.insertCell(colCount);
            cell.contentEditable = "true";
            cell.id = `cell-${i}-${colCount}`;
        }
    };

    window.changeFontSize = function () {
        if (selectedCell) {
            let size = document.getElementById("fontSize").value;
            selectedCell.style.fontSize = size;
        }
    };

    window.changeFontColor = function () {
        if (selectedCell) {
            let color = document.getElementById("fontColor").value;
            selectedCell.style.color = color;
        }
    };


    window.trimText=function() {
        if (selectedCell) {
            selectedCell.innerText = selectedCell.innerText.trim();
        }
    };

     window.convertText=function(type) {
        if (selectedCell) {
            selectedCell.innerText = type === 'upper' ? selectedCell.innerText.toUpperCase() : selectedCell.innerText.toLowerCase();
        }
    };

    window.removeDuplicates=function() {
        let seen = new Set();
        document.querySelectorAll("td").forEach(cell => {
            if (seen.has(cell.innerText)) {
                cell.innerText = "";
            } else {
                seen.add(cell.innerText);
            }
        });
    };

    window.findAndReplace=function() {
        let findText = prompt("Enter text to find:");
        let replaceText = prompt("Enter replacement text:");
        if (findText !== null && replaceText !== null) {
            document.querySelectorAll("td").forEach(cell => {
                if (cell.innerText.includes(findText)) {
                    cell.innerText = cell.innerText.replace(new RegExp(findText, 'g'), replaceText);
                }
            });
        }
    };

    window.calculate=function(operation) {
        if (!selectedCell) return;
        let value = parseFloat(selectedCell.innerText);
        if (isNaN(value)) return;
        switch (operation) {
            case 'ROUND':
                selectedCell.innerText = Math.round(value);
                break;
            case 'ABS':
                selectedCell.innerText = Math.abs(value);
                break;
            case 'SQRT':
                selectedCell.innerText = Math.sqrt(value).toFixed(2);
                break;
        }
    };

    window.validateInput= function(cell) {
        let value = cell.innerText.trim();
        if (!isNaN(value) && value !== "") {
            cell.dataset.type = "number";
        } else if (!isNaN(Date.parse(value))) {
            cell.dataset.type = "date";
        } else {
            cell.dataset.type = "text";
        }
    };

    window.saveSpreadsheet = function () {
        let sheetElement = document.getElementById("spreadsheet");
        if (!sheetElement) {
            console.error("❌ Spreadsheet element not found!");
            return;
        }
    
        let sheetId = sheetElement.dataset.sheetId;
        if (!sheetId) {
            console.error("❌ Sheet ID is missing!");
            return;
        }
    
        let sheetName = document.getElementById("sheet-name")?.innerText.trim() || "Untitled Sheet";
        let data = [];
    
        document.querySelectorAll("td").forEach(cell => {
            if (cell.id && cell.id.startsWith("cell-")) {
                let parts = cell.id.split("-");
                if (parts.length === 3) {
                    let row = parseInt(parts[1], 10);
                    let col = parseInt(parts[2], 10);
                    data.push({ row, col, value: cell.innerText });
                }
            }
        });
    
        let csrfToken = getCSRFToken(); // Ensure this function is defined somewhere
    
        fetch("http://127.0.0.1:8000/sheets/api/save-sheet/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({
                sheet_id: sheetId,
                name: sheetName,
                cells: data
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            alert("✅ Spreadsheet saved successfully!");
        })
        .catch(error => {
            console.error("❌ Error saving spreadsheet:", error);
            alert("❌ Failed to save spreadsheet. Check console for details.");
        });
    };

    window.loadSpreadsheet = function() {
        let sheetElement = document.getElementById("spreadsheet");
        if (!sheetElement) {
            console.error("❌ Spreadsheet element not found!");
            return;
        }
    
        let sheetId = sheetElement.dataset.sheetId;  // ✅ Correctly get the sheet ID
        if (!sheetId) {
            console.error("❌ Sheet ID is missing!");
            return;
        }
    
        fetch(`/sheets/load/${sheetId}/`)
            .then(response => response.json())
            .then(data => {
                data.cells.forEach(cell => {
                    let cellElement = document.getElementById(cell.id);
                    if (cellElement) {
                        cellElement.innerText = cell.value;  // ✅ Populate saved values
                    }
                });
                console.log("✅ Spreadsheet loaded successfully.");
            })
            .catch(error => console.error("❌ Error loading spreadsheet:", error));
    };

    window.getCSRFToken = function() {
        return document.cookie.split('; ').find(row => row.startsWith('csrftoken'))?.split('=')[1] || "";
    };
    

    // Assign function globally so it's accessible in HTML
    window.validateInput = validateInput;
});
