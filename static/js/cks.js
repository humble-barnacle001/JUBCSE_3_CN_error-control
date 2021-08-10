const cks = (init_data, bits = 16) => {
    const data =
        init_data +
        (init_data.length % bits
            ? "0".repeat(bits - (init_data.length % bits))
            : "");
    console.log(`${bits} bits checksum`);
    let sum = 0;
    for (let i = 0; i < data.length / bits; i++) {
        sum = sum + parseInt(data.substring(i * bits, (i + 1) * bits), 2);
    }

    while (sum > 2 ** bits - 1) {
        sum = (sum % (2 ** bits - 1)) + parseInt(sum / (2 ** bits - 1));
    }
    sum = sum ^ (2 ** bits - 1);

    return data + dec2bin(sum, bits);
};
