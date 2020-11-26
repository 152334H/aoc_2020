const fs = require('fs');
fs.readFile('input', (_, d) => {
    let s2 = d.toString().slice(0, -1);
    s1 = s2+s2[0];
    console.log(Array.from({length: s1.length-1}, (_,i) => Number(s1.slice(i,i+2)))
                .filter(v => v%11==0)
                .map(v => v/11)
                .reduce((a,b) => a+b)
    );
    console.log(Array.from(s2, (c,i) => c == s2[(i+s2.length/2)%s2.length] ? Number(c) : 0)
                .reduce((a,b) => a+b)
    );
});
