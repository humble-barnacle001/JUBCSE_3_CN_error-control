const getLength = (n) => {
    let s = 0;
    for (let i = n; i > 0; i /= 10, s++);
    return s;
};

const dec2bin = (d, c = 8) => {
    let bin = "";
    while (d != 0) {
        bin = (d % 2) + bin;
        d = parseInt(d / 2);
    }
    return (
        (bin.length % c || bin.length == 0
            ? "0".repeat(c - (bin.length % c))
            : "") + bin
    );
};

const bin2hex = (b) => {
    const l = [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f"
    ];
    let hex = "";
    for (let i = 0; i < b.length; i += 4) {
        hex += l[parseInt(b.substr(i, 4), 2)];
    }
    return hex;
};

function smoothScroll(target) {
    var scrollContainer = target;
    do {
        //find scroll container
        scrollContainer = scrollContainer.parentNode;
        if (!scrollContainer) return;
        scrollContainer.scrollTop += 1;
    } while (scrollContainer.scrollTop == 0);

    var targetY = 0;
    do {
        //find the top of target relatively to the container
        if (target == scrollContainer) break;
        targetY += target.offsetTop;
    } while ((target = target.offsetParent));

    scroll = function (c, a, b, i) {
        i++;
        if (i > 30) return;
        c.scrollTop = a + ((b - a) / 30) * i;
        setTimeout(function () {
            scroll(c, a, b, i);
        }, 20);
    };
    // start scrolling
    scroll(scrollContainer, scrollContainer.scrollTop, targetY, 0);
}
