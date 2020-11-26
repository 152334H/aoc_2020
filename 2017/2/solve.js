const fs = require('fs');
fs.readFile('input', (_, d) => {
    // parse input
    let lines = d.toString().trim().split('\n').map(
        l => l.split('\t').map(n => Number(n)).sort((a,b) => a-b)
    ); /* lines=[[10, 27, ..., 294], ...] Each inner array is sorted. */
    // part 1
    console.log(lines.map(
        l => l.slice(-1)-l[0]   // [last elem] - first elem == max-min
    ).reduce((a,b) => a+b));
    // part 2
    console.log(lines.flatMap(l => l.flatMap(
        // due to sorting, w > v is guaranteed.
        (v,i) => l.slice(i+1).filter(w => w%v == 0).map(w => w/v)
    )).reduce((a,b) => a+b));
});
