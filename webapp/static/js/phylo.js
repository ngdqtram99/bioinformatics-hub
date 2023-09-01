/**Dieses Skript wird verwendet, um Iterations Tabellen bei upgma/nj zu zeichnen
 * Im Template müssen folgende Elemente vorhanden sein:
 * - div mit id 'tables-container'
 * Im Template-Skript müssen außerdem folgende Variablen deklariert werden:
 * var iterations 
 * iterations müssen den Aufbau wie im folgendem Beispiel haben:
 * bei upgma:
 * [{'names': ['A', 'B', 'C', 'D', 'E'], 'matrix': [[0], [3.99999, 0], [7.0, 8.0, 0], [9.0, 10.0, 10.0, 0], [8.0, 9.0, 9.0, 5.0, 0]], 'min_dist': 3.99999}, {'names': ['(B,A)', 'C', 'D', 'E'], 'matrix': [[0], [7.5, 0], [9.5, 10.0, 0], [8.5, 9.0, 5.0, 0]], 'min_dist': 5.0}, {'names': ['(B,A)', 'C', '(E,D)'], 'matrix': [[0], [7.5, 0], [9.0, 9.5, 0]], 'min_dist': 7.5}, {'names': ['(C,(B,A))', '(E,D)'], 'matrix': [[0], [9.166666666666666, 0]], 'min_dist': 9.166666666666666}, {'names': ['((E,D),(C,(B,A)))'], 'matrix': [[0]]}]
 * bei nj:
 * [{'names': ['r', 'a', 'b', 'C', 'd', 'r'], 'matrix': [[0], [3.0, 0], [7.0, 8.0, 0], [9.0, 10.0, 10.0, 0], [8.0, 9.0, 9.0, 5.0, 0], [9, 10, 11, 11, 10]], 'edited_matrix': [[0], [-16.0, 0], [-13.0, -13.0, 0], [-11.0, -11.0, -12.0, 0], [-11.0, -11.0, -12.0, -16.0, 0]], 'edited_min_dist': -16.0}, {'names': ['(r,a)', 'b', 'C', 'd', 'r'], 'matrix': [[0], [6.0, 0], [8.0, 10.0, 0], [7.0, 9.0, 5.0, 0], [10, 12, 11, 10]], 'edited_matrix': [[0], [-16.0, 0], [-13.0, -13.0, 0], [-13.0, -13.0, -16.0, 0]], 'edited_min_dist': -16.0}, {'names': ['((r,a),b)', 'C', 'd', 'r'], 'matrix': [[0], [6.0, 0], [5.0, 5.0, 0], [11, 11, 10]], 'edited_matrix': [[0], [-16.0, 0], [-16.0, -16.0, 0]], 'edited_min_dist': -16.0}, {'names': ['(((r,a),b),C)', 'd'], 'matrix': [[0], [2.0, 0]]}] 
 * var algorithm = "upgma" oder "nj", je nach template
 */
function createTables(iterations) {
    var tablesContainer = document.getElementById('tables-container');

    iterations.forEach((iteration, index) => {
        var iterationHeader = document.createElement('p');
        iterationHeader.style.fontWeight = 'bold';
        iterationHeader.textContent = (index + 1) + '. Iteration:'; 
        tablesContainer.appendChild(iterationHeader);

        var table = document.createElement('table');
        table.classList.add('dist-table');
        var tr = document.createElement('tr');
        var thEmpty = document.createElement('th');
        thEmpty.textContent = '';
        tr.appendChild(thEmpty);

        iteration.names.forEach((name, index) => {
            if (index == iteration.names.length-1 && algorithm == 'nj' && name == 'r'){

            } else{
            var th = document.createElement('th');
            th.textContent = name;
            tr.appendChild(th);}
        });

        table.appendChild(tr);

        for (var i = 0; i < iteration.matrix.length; i++) {
            var tr = document.createElement('tr');
            var tdName = document.createElement('td');
            tdName.textContent = iteration.names[i];
            tr.appendChild(tdName);

            for (var j = 0; j < iteration.matrix[i].length; j++) {
                var td = document.createElement('td');
                var originalValue = iteration.matrix[i][j];
                var floatPart = getFloatPart(originalValue);
                if (floatPart.length > 2) {
                  // Wenn die Zahl mehr als zwei Dezimalstellen hat
                  td.title = originalValue.toString(); // Füge das title-Attribut hinzu
                  td.textContent = originalValue.toFixed(2);
                } else {
                  // Wenn die Zahl eine ganze Zahl ist oder weniger als 2 Nachkommastellen hat, keine Kürzung erforderlich
                  td.textContent = originalValue
                } 
                tr.appendChild(td);
            }
            var x = 0;
            if (algorithm == "nj" && index != iterations.length-1) {
                x = -1;
            }
            for (var j = 0; j < iteration.matrix.length-iteration.matrix[i].length+x; j++) { //füge fehlende leere tds
                var td = document.createElement('td');
                tr.appendChild(td);}
            table.appendChild(tr);
        }
        tablesContainer.appendChild(table);
        
        if (iteration.min_dist != null ) {
        var minDistRow = document.createElement('p');
        
        if (getFloatPart(iteration.min_dist).length > 2){
            minDistRow.title = iteration.min_dist;
            minDistRow.textContent = 'Minimale Distanz: '+iteration.min_dist.toFixed(2); }
            else{minDistRow.textContent = 'Minimale Distanz: '+iteration.min_dist;}
        tablesContainer.appendChild(minDistRow);
        
            
        }     
        tablesContainer.appendChild(document.createElement('br'));
        
        if (algorithm == 'nj' && index!=iterations.length-1) {
        var iterationHeader = document.createElement('p');
        
        iterationHeader.textContent = 'Korrigierte Matrix:'; 
        tablesContainer.appendChild(iterationHeader);
        var table = document.createElement('table');
        table.classList.add('dist-table');
        var tr = document.createElement('tr');
        var thEmpty = document.createElement('th');
        thEmpty.textContent = '';
        tr.appendChild(thEmpty);

        iteration.names.forEach((name, index) => {
            if (index!=iteration.names.length-1){
            var th = document.createElement('th');
            th.textContent = name;
            tr.appendChild(th);}
        });

        table.appendChild(tr);

        for (var i = 0; i < iteration.edited_matrix.length; i++) {
            var tr = document.createElement('tr');
            var tdName = document.createElement('td');
            tdName.textContent = iteration.names[i];
            tr.appendChild(tdName);

            for (var j = 0; j < iteration.edited_matrix[i].length; j++) {
                var td = document.createElement('td');
                var originalValue = iteration.edited_matrix[i][j];
                var floatPart = getFloatPart(originalValue);
                if (floatPart.length > 2) {
                  // Wenn die Zahl mehr als zwei Dezimalstellen hat
                  td.title = originalValue.toString(); // Füge das title-Attribut hinzu
                  td.textContent = originalValue.toFixed(2);
                } else {
                  // Wenn die Zahl eine ganze Zahl ist oder weniger als 2 Nachkommastellen hat, keine Kürzung erforderlich
                  td.textContent = originalValue
                } 
                tr.appendChild(td);
            }
            
            for (var j = 0; j < iteration.edited_matrix.length-iteration.edited_matrix[i].length; j++) { //füge fehlende leere tds
                var td = document.createElement('td');
                tr.appendChild(td);}
            table.appendChild(tr);
        }
        tablesContainer.appendChild(table);
        
        if (iteration.edited_min_dist != null ) {
        var minDistRow = document.createElement('p');
        
        if (getFloatPart(iteration.min_dist).length > 2){
            minDistRow.title = iteration.edited_min_dist;
            minDistRow.textContent = 'Minimale Distanz: '+iteration.edited_min_dist.toFixed(2); }
            else{minDistRow.textContent = 'Minimale Distanz: '+iteration.edited_min_dist;}
        tablesContainer.appendChild(minDistRow);           
        }     
        tablesContainer.appendChild(document.createElement('br'));
        }
    });
}
function getFloatPart(originalValue){

    let floatPart= (originalValue + "").split(".")[1];
    if (floatPart == undefined){
        floatPart = "";
    }
    return floatPart;
}
createTables(iterations);