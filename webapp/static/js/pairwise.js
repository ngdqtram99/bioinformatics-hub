/*
Dieses Skript wird verwendet, um Alignments, die Score-Tabelle und Pfade in den Alignment-Templates zu zeichnen.
Dieses Skript ermöglicht auch, dass ein Alignment in der Alignments-Tabelle ausgewählt werden kann und der dazugehörige Pfad wird in der Score-Tabelle gezeichnet.

Der Template muss eine Tabelle und einen div-Container mit bestimmten ids enthalten:
<table id="matrixTable"> 
<div id="alignmentsContainer">
Es muss auch ein Checkbox <input type="checkbox" id="showArrows"> im Template vorhanden sein  

Desweiteren sollen CSS-Klassen .path, .alignment, .alignment.selected, .hor, .vert und .diag, .duaghorvert, .horvert und .diaghor definiert sein

Folgende Variablen müssen im Template initialisiert werden:

matrixValues - die Score-Matrix in Form von Listen von Listen (eigene Liste für jede Zeile)
    Beispiel von matrixValues = [ 
            [0, -10, -20, -30, -40],
            [-10, 1, -9, -19, -29],
            [-20, -9, 2, -8, -18],
            [-30, -19, -8, 1, -9],
            [-40, -29, -18, -7, 0],
            [-50,-39,-28,-17,-6]
            ] 
alignments - Eine Liste von dictionaries für jeden Alignment. Aufgebaut wie folgt:
    [{'alignment':[], 'path':[]}, {'alignment':[], 'path':[]},…] 

firstSequence - Eine Liste aus der Buchstaben der ersten Sequenz, z.B. ['A', 'B', 'C', 'C']

secondSequence - Eine Liste aus der Buchstaben der zweiten Sequenz

tracebackMatrix - Die Traceback-Matrix mit Bezeichnungen von Richtungen in Form von Listen von Listen (eigene Liste für jede Zeile)
                  Sind es zwei oder mehr mögliche Richtungen, so sollen die an der Stelle als Liste, die Ordnung ist dabei nicht wichtig
    Beispiel von tracebackMatrix = 
    [['', 'hor', 'hor', 'hor'], 
    ['vert', 'diag', ['diag', 'hor'], 'diag'], 
    ['vert', ['diag', 'vert'], 'diag', ['diag', 'vert', 'hor']], 
    ['vert', 'diag', 'diag', ['diag', 'hor']], 
    ['vert', ['diag', 'vert'], 'diag', ['diag', 'hor']]]

    Dabei besteht jeder Alignment aus einer Liste von Strings
    Der erste String ist die Sequenz 1 nach dem Alignment (also mit ggf. eingefügten Gaps) 
    Der zweite String besteht aus Leerzeichen und '|' - Zeichen, dabei steht | überall an den Positionen, wo Sequenz 1 nach dem Alignment mit der Sequenz 2 nach dem Alignment übereinstimmt
    Der dritte String ist Sequenz 2 nach dem Alignment
    Beispiel: 'alignment': ['--CC', '  ||', 'BBCC']
Der Path enthält eine Liste von Listen, die die Positionen in der Matrix beschreiben, durch die der Pfad verläuft. Zusätzlich enthält jede liste einen String mit der Richting
    Beispiel: 'path': [[[2, 4], 'diag'], [[1, 3], 'diag'], [[0, 2], 'hor'], [[0, 1], 'hor'], [[0, 0]]]
    Erlaubte Richtingen sind 'hor' für Horizontal, 'vert' für Vertikal und 'diag' für Diagonal. Die Richting darf auch fehlen*/

var path = alignments[0].path;
var selectedAlignmentRow = document.querySelector(".alignment.selected");
var selectedPath = null;
var selectedCell = document.querySelector(".selectedcell");
// Funktion, um die Tabelle zu erstellen und den Pfad mit Klassen für die Pfeile zu markieren
function createMatrixTable() {
  const showArrowsCheckbox = document.getElementById("showArrows");
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

        if (coords[0] === i - 1 && coords[1] === j - 1) {
          cell.classList.add("path");
          if (direction) {
            cell.classList.add(`${direction}`);
          }
          break;
        }
      }

      if (!isNaN(cell.textContent) && cell.textContent != "") {
        cell.setAttribute("row", i - 1);
        cell.setAttribute("col", j - 1);
        cell.addEventListener("click", () => {
          var checkBox = document.getElementById("showArrows");
          // Klasse vom bereits gewählter Zeile löschen
          if (selectedCell != null) {
            selectedCell.classList.remove("selectedcell");
            if (!checkBox.checked) {
              selectedCell.classList.remove(
                "diag",
                "hor",
                "vert",
                "diagvert",
                "diaghor",
                "diaghorvert",
                "horvert"
              );
            }
            if (selectedCell.classList.contains("path")) {
              applyNewPath(selectedPath);
            }
          }
          if (selectedCell != cell) {
            // Neue als selected markieren
            cell.classList.add("selectedcell");
            selectedCell = cell;
            addArrowClasses(cell.getAttribute("row"), cell.getAttribute("col"));
            //selectedPath = path;
            //applyNewPath(path);
          } else {
            selectedCell = null;
            cell.classList.remove("selectedcell");
            
            if (!checkBox.checked) {
              cell.classList.remove(
                "diag",
                "hor",
                "vert",
                "diagvert",
                "diaghor",
                "diaghorvert",
                "horvert"
              );
            }
            if (cell.classList.contains("path")) {
              console.log("Path");
              applyNewPath(selectedPath);
            }
          }
        });
      }
      row.appendChild(cell);
    }
    table.appendChild(row);
  }
}

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
    alignmentRow.classList.add("alignment");

    if (i === 0 && selectedAlignmentRow == null) {
      alignmentRow.classList.add("selected");
      selectedPath = path;
    }

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
    selectedAlignmentRow = document.querySelector(".alignment.selected");

    // der Klick-Event-Listener, um den Pfad zu ändern
    alignmentRow.addEventListener("click", () => {
      // Klasse vom bereits gewählter Zeile löschen
      if (selectedAlignmentRow != null) {
        selectedAlignmentRow.classList.remove("selected");
      }
      if (selectedAlignmentRow != alignmentRow) {
        // Neue als selected markieren
        alignmentRow.classList.add("selected");
        selectedAlignmentRow = alignmentRow;
        selectedPath = path;
        applyNewPath(path);
      } else {
        selectedAlignmentRow = null;
        applyNewPath([]);
      }
    });
  }
}

// Funktion zum Anwenden eines neuen Pfades in der Matrix-Tabelle
function applyNewPath(path) {
  const matrixTable = document.getElementById("matrixTable");
  const showArrowsCheckBox = document.getElementById("showArrows");
  // Entferne vorherige path-Klassen
  const cells = matrixTable.querySelectorAll("td");
  if (!showArrowsCheckBox.checked) {
    cells.forEach((cell) => {
      if (!cell.classList.contains("selectedcell")) {
      cell.classList.remove("path", "diag", "hor", "vert");}
    });
  } else {
    cells.forEach((cell) => {
      cell.classList.remove("path");
    });
  }
  // Füge die neuen path-Klassen hinzu
  for (let k = 1; k <= path.length; k++) {
    const [coords, direction] = path[k - 1];
    const rowIndex = coords[0] + 1;
    const colIndex = coords[1] + 1;
    const cell = matrixTable.rows[rowIndex].cells[colIndex];

    cell.classList.add("path");

    if (!showArrowsCheckBox.checked) {
      if (direction) {
        cell.classList.add(direction);
      }
    }
  }
}
function addArrowClasses(k, n) {
  console.log(k, n);
  const matrixTable = document.getElementById("matrixTable");
  const cells = matrixTable.querySelectorAll("td");
  const coords = [k, n];
  var direction = tracebackMatrix[k][n];

  const rowIndex = Number(coords[0]) + 1;
  const colIndex = Number(coords[1]) + 1;
  console.log(rowIndex);
  const cell = matrixTable.rows[rowIndex].cells[colIndex];
  if (Array.isArray(direction)) {
    direction = direction.sort();
    direction = direction.join("");
  }

  if (direction != "") {
    cell.classList.add(direction);
  }
}
function showArrows(checked) {
  const matrixTable = document.getElementById("matrixTable");

  var cells = matrixTable.querySelectorAll("td");
  
  cells.forEach((cell) => {
    if (!cell.classList.contains("selectedcell")) {
      console.log(cell);
      cell.classList.remove(
        "diag",
        "hor",
        "vert",
        "diagvert",
        "diaghor",
        "diaghorvert",
        "horvert"
      );
    }
  });
  
  if (checked) {
    // Füge die neuen Klassen mit Richtungen aus der Traceback Matrix hinzu
    for (let k = 0; k < tracebackMatrix.length; k++) {
      for (n = 0; n < tracebackMatrix[k].length; n++) {
        addArrowClasses(k, n);
      }
    }
  } else if (selectedAlignmentRow != null) {
    applyNewPath(selectedPath);
  }
}

// Event-Listener für den Checkbox-Status
showArrowsCheckbox.addEventListener("change", () => {
  var checkBox = document.getElementById("showArrows");
  if (checkBox.checked) {
    showArrows(true);
  } else {
    showArrows(false);
  }
});
showAlignments();
createMatrixTable();
