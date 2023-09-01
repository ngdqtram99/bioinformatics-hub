/**
 * Dieses Skript wird verwendet, um Paths und  die probability matrix Tabellen  zu zeichnen.
 * Dieses Skript ermöglicht auch, dass ein Pfad in der Pfad-Tabelle ausgewählt werden kann und der dazugehörige Pfad wird in der Matrix-Tabelle gezeichnet.
 * Im Template müssen folgende Elemente vorhanden sein:
 * tables mit ids probabilityMatrixTable und logProbabilityMatrixTable, paths-table
 * Im Template-Skript müssen außerdem folgende Variablen deklariert werden:
 * seq - die vom user eingegebene sequenz
 * data - daten aus dem backend, enthalt eine liste von dictionaries die jeweils einen 'states' key mit einer liste von states und 'path' key, der eine liste aus [zeile,spalte] koordinaten enthält 
 * pathTable - document.getElementById('paths-table')
 */
var selectedPathRow = document.querySelector(".path-element.selected");
      
for (var i = 0; i < data.length; i++) {
    var row = pathTable.insertRow();        
    var combinedStrings = seq + "<br>" + data[i].states.join('');

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