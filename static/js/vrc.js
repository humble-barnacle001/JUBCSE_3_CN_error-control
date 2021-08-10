const vrc = (data, parity = "Even") => {
    console.log(`${parity} parity VRC`);
    return data + ((data.split("1").length - (parity === "Even" ? 1 : 0)) % 2);
};
