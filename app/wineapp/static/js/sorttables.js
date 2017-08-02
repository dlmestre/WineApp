function sortNumbers(item) {
   return parseFloat(row.cells[col].textContent);
}

function sorTable(table,col,reverse) {
    var tb = table.tBodies[0];
    tr = Array.prototype.slice.call(tb.rows,0);
    var i;
    reverse = -((+reverse) || -1);
    tr = tr.sort(function(a,b) {
        try {
            console.log("working");
            
            //part1 = parseFloat(a.cells[col].textContent.trim());
            //part2 = parseFloat(b.cells[col].textContent.trim());
            //return reverse * parseFloat(a.cells[col].textContent.trim().localeCompare(b.cells[col].textContent.trim()));         
        }
        catch(err) {
            console.log(err);
            return reverse * (a.cells[col].textContent.trim().localeCompare(b.cells[col].textContent.trim()));
        }
        //return reverse * (a.cells[col].textContent.trim().localeCompare(b.cells[col].textContent.trim()));
    });
    for(i=0;i<tr.length;++i) {
        tb.appendChild(tr[i]);
    }
}

function makeSortable(table) {
    var th = table.tHead;
    var i;
    th && (th = th.rows[0]) && (th = th.cells);
    if (th) i = th.length;
    else return;
    while (--i>=0) (function(i) {
        var dir = 1;
        th[i].addEventListener('click',function() {
            sorTable(table,i,(dir = 1 -dir));
        });
    }(i));
}

function makeAllSortable(parent) {
    parent = parent || document.body;
    var t = parent.getElementsByTagName('table'), i = t.length;
    while (--i>=0) makeSortable(t[i]);
}

function makeAllSortable2() {
    parent = document.body;
    var t = parent.getElementsByTagName('table'), i = t.length;
    while (--i>=0) makeSortable(t[i]);
}

/* window.onload = function () {makeAllSortable();}; */
