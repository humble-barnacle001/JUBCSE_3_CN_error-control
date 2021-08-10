const lrc = (init_data, bits = 8) => {
    console.log(`${bits} bits LRC`);
    // Uses end padding
    const data =
        init_data +
        (init_data.length % bits
            ? "0".repeat(bits - (init_data.length % bits))
            : "");
    let lrc = 0;
    for (let i = 0; i < data.length / bits; i++) {
        lrc =
            (lrc + parseInt(data.substring(i * bits, (i + 1) * bits), 2)) &
            (2 ** bits - 1);
    }
    lrc = ((lrc ^ (2 ** bits - 1)) + 1) & (2 ** bits - 1);
    return data + dec2bin(lrc, bits);
};
