function createTables(iterations) {
    var tablesContainer = document.getElementById('tables-container');

    iterations.forEach(iteration => {
        var table = document.createElement('table');
        table.classList.add('dist-table');
        var tr = document.createElement('tr');
        var thEmpty = document.createElement('th');
        thEmpty.textContent = '';
        tr.appendChild(thEmpty);

        iteration.names.forEach(name => {
            var th = document.createElement('th');
            th.textContent = name;
            tr.appendChild(th);
        });

        table.appendChild(tr);

        for (var i = 0; i < iteration.matrix.length; i++) {
            var tr = document.createElement('tr');
            var tdName = document.createElement('td');
            tdName.textContent = iteration.names[i];
            tr.appendChild(tdName);

            for (var j = 0; j < iteration.matrix[i].length; j++) {
                var td = document.createElement('td');
                td.textContent = iteration.matrix[i][j].toFixed(2);
                tr.appendChild(td);
            }

            table.appendChild(tr);
        }

        var minDistRow = document.createElement('tr');
        var minDistLabel = document.createElement('td');
        minDistLabel.textContent = 'min_dist';
        minDistRow.appendChild(minDistLabel);

        var minDistValue = document.createElement('td');
        minDistValue.textContent = iteration.min_dist.toFixed(2);
        minDistRow.appendChild(minDistValue);

        table.appendChild(minDistRow);

        tablesContainer.appendChild(table);
        tablesContainer.appendChild(document.createElement('br'))
    });
}
createTables(iterations);