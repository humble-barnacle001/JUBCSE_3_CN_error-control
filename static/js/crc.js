const crc = (init_data, divisor) => {
    console.log(`CRC polynomial: ${divisor}`);
    const data = init_data + "000";
    let remainder = Array.from(data.slice(0, divisor.length));
    for (let i = 0; i < data.length - divisor.length + 1; i++) {
        if (remainder[0] === "1") {
            for (let j = 1; j < divisor.length; j++) {
                remainder[j - 1] = remainder[j] === divisor[j] ? "0" : "1";
            }
        } else {
            for (let j = 1; j < divisor.length; j++) {
                remainder[j - 1] = remainder[j];
            }
        }
        remainder[divisor.length - 1] = data[i + divisor.length];
    }
    return init_data + remainder.join("");
};
