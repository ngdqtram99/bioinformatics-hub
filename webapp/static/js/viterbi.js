var selectedPathRow = document.querySelector(".path-element.selected");
      
for (var i = 0; i < data.length; i++) {
    var row = pathTable.insertRow();        
    var combinedStrings = symbols.join('') + "<br>" + data[i].states.join('');

    var combinedCell = row.insertCell();
    combinedCell.innerHTML = combinedStrings;
    row.classList.add('path-element');
    if (i === 0 && selectedPathRow == null) {
        row.classList.add("selected");
        markCellsInTable('probabilityMatrixTable', data[0].path);
        markCellsInTable('logProbabilityMatrixTable', data[0].path);
      }

      row.addEventListener('click', function(event) {
        resetCells();
        var selectedPathRow = document.querySelector(".path-element.selected");
        var clickedRow = event.currentTarget;
        if (selectedPathRow != null) {
            selectedPathRow.classList.remove("selected");
            if (clickedRow == selectedPathRow) {
                applyNewPath([]);
            }
            else {
                clickedRow.classList.add("selected");            
                applyNewPath(data[clickedRow.rowIndex].path);
            }                   
        }
        else{
            clickedRow.classList.add("selected");            
            applyNewPath(data[clickedRow.rowIndex].path);
        }        
    });
}

  function applyNewPath(path) {
    markCellsInTable('probabilityMatrixTable', path);
    markCellsInTable('logProbabilityMatrixTable', path);
  }

  function markCellsInTable(tableId, coordinates) {
    var table = document.getElementById(tableId);
    for (var i = 0; i < coordinates.length; i++) {
      var row = coordinates[i][0]+1;
      var col = coordinates[i][1]+1;
      var cell = table.rows[row].cells[col];
      cell.classList.add('path');
    }
  }

  function resetCells() {
    var cells = document.querySelectorAll('.path');
    cells.forEach(function(cell) {
      cell.classList.remove('path');
    });
   
  }