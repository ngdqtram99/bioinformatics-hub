const path = alignments[0].path;
    
// Funktion, um die Tabelle zu erstellen und den Pfad mit Klassen für die Pfeile zu markieren
function createMatrixTable() {
    const table = document.getElementById("matrixTable");

    for (let i = 0; i < firstSequence.length; i++) {
    const row = document.createElement("tr");

    for (let j = 0; j < secondSequence.length; j++) {
        const cell = document.createElement("td");

        if (i === 0 && j >= 0) {
        // Zeilen- und Spaltenbeschriftungen einfügen
        cell.textContent = secondSequence[j];
        } else if (i > 0 && j === 0) {
        cell.textContent = firstSequence[i];
        } else if (i > 0 && j > 0) {
        // Scores in die Zellen einfügen

        cell.textContent = matrixValues[i - 1][j - 1];
        }

        // Prüfen, ob die Zelle zum Pfad gehört und füge die Klasse path hinzu
        for (let k = 1; k <= path.length; k++) {
        const [coords, direction] = path[k - 1];

        if (coords[0] === i-1 && coords[1] === j-1) {
            cell.classList.add('path');
            if (direction) {
            cell.classList.add(`${direction}`);
            }
            break;
        }
        }

        row.appendChild(cell);
    }

    table.appendChild(row);
    }
}    
        
let selectedAlignmentRow = document.querySelector(".alignment.selected");
// Funktion zum Anzeigen der Alignments
function showAlignments() {
    const alignmentsContainer = document.getElementById("alignmentsContainer");
    
    // Entferne vorherige Inhalte im Container
    alignmentsContainer.innerHTML = "";
    const alignmentTable = document.createElement("table");
    alignmentTable.classList.add("alignment-table");
    // Iteriere durch die Alignments und füge sie der Tabelle hinzu
    for (let i = 0; i < alignments.length; i++) {
        const alignment = alignments[i].alignment;
        const path = alignments[i].path;
        
        
        
        const alignmentRow = document.createElement("tr");
        alignmentRow.classList.add('alignment');
          
        
        if (i===0 && selectedAlignmentRow == null){
            alignmentRow.classList.add('selected');
            
        }
        selectedAlignmentRow = document.querySelector(".alignment.selected");
        console.log(selectedAlignmentRow)
        const alignmentCell = document.createElement("td");
    
        alignment.forEach((line, index) => {
          const lineText = document.createTextNode(line);
          alignmentCell.appendChild(lineText);
    
          if (index < alignment.length - 1) {
            alignmentCell.appendChild(document.createElement("br"));
          }
        });
    
        alignmentRow.appendChild(alignmentCell);
        alignmentTable.appendChild(alignmentRow);
        alignmentsContainer.appendChild(alignmentTable);

      // der Klick-Event-Listener, um den Pfad zu ändern
      alignmentRow.addEventListener("click", () => {
        // Klasse vom bereits gewählter Zeile löschen
        selectedAlignmentRow.classList.remove("selected");
        // Neue als selected markieren
        alignmentRow.classList.add("selected");
        selectedAlignmentRow = alignmentRow;
        applyNewPath(path);
      });
    }
  }

  // Funktion zum Anwenden eines neuen Pfades in der Matrix-Tabelle
  function applyNewPath(path) {
    const matrixTable = document.getElementById("matrixTable");

    // Entferne vorherige path-Klassen
    const cells = matrixTable.querySelectorAll("td");
    cells.forEach((cell) => {
      cell.classList.remove("path", "diag", "hor", "vert");
    });

    // Füge die neuen path-Klassen hinzu
    for (let k = 1; k <= path.length; k++) {
      const [coords, direction] = path[k - 1];
      const rowIndex = coords[0] + 1;
      const colIndex = coords[1] + 1;
      const cell = matrixTable.rows[rowIndex].cells[colIndex];

      cell.classList.add("path");
      if (direction) {
        cell.classList.add(direction);
      }
    }
  }

  showAlignments();
  createMatrixTable();