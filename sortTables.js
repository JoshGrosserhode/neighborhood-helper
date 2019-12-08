         // sort table
      function sortTable() {
        var table, rows, switching, n, x, y, shouldSwitch;
        table = document.getElementById("index_table");
        switching = true;
        /* Make a loop that will continue until
        no switching has been done: */
        while (switching) {
          // Start by saying: no switching is done:
          switching = false;
          rows = table.rows;
          /* Loop through all table rows (except the
          first, which contains table headers): */
          for (n = 1; n < (rows.length - 1); n++) {
            // Start by saying there should be no switching:
            shouldSwitch = false;
            /* Get the two elements you want to compare,
            one from current row and one from the next: */
            x = rows[n].getElementsByTagName("td")[0];
            y = rows[n + 1].getElementsByTagName("td")[0];
            // Check if the two rows should switch place:
            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
              // If so, mark as a switch and break the loop:
              shouldSwitch = true;
              break;
            }
          }
          if (shouldSwitch) {
            /* If a switch has been marked, make the switch
            and mark that a switch has been done: */
            rows[n].parentNode.insertBefore(rows[n + 1], rows[n]);
            switching = true;
          }
        }
      }