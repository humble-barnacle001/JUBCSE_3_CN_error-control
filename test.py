from application.cks import cks_verify
from application.lrc import lrc_verify
from application.vrc import vrc_verify
from application.crc import crc_verify
from plot_rate import pie_plot

import random
import csv
import matplotlib.pyplot as plt
from pathlib import Path


def random_stream(n: int) -> str:
    x = bin(random.getrandbits(n))[2:]
    return "0"*(n-len(x))+x


def avg(l):
    return sum(map(float, l))/len(l)


def plot(n, f, m, x):
    ls = ["-", "--", "-.", ":"]
    for i in range(len(f[0])):
        plt.plot(
            x, list(map(lambda x: int(x[i]), f)), linestyle=ls[i % len(ls)])
    plt.legend(m)
    plt.xlabel("bits after encoding")
    plt.ylabel("time in nanoseconds")
    plt.title(n)
    plt.savefig("results/"+n+".png", bbox_inches='tight')
    print("Plotted for", n)
    plt.clf()


if __name__ == "__main__":
    x = 2**15
    d = []
    cks = []
    lrc = []
    vrc = []
    crc = []

    cks_meta = []
    lrc_meta = []
    vrc_meta = []
    crc_meta = []

    i = 128
    while(i <= x):
        d.append(random_stream(i))
        i = i*2

    Path("results").mkdir(parents=True, exist_ok=True)

    with open("results/cks.csv", "w") as res:
        resWrite = csv.writer(res)
        cks_meta = ["8-bit", "16-bit", "32-bit", "64-bit"]
        resWrite.writerow(["bits"]+cks_meta)
        for data in d:
            print(len(data))
            t = list(map(
                lambda b: str(cks_verify(data, b)[0]), [8, 16, 32, 64]))
            cks.append(t)
            resWrite.writerow([len(data)]+t)

    with open("results/lrc.csv", "w") as res:
        resWrite = csv.writer(res)
        lrc_meta = ["8-bit", "16-bit", "32-bit", "64-bit"]
        resWrite.writerow(["bits"]+lrc_meta)
        for data in d:
            print(len(data))
            t = list(
                map(lambda b: str(lrc_verify(data, b)[0]), [8, 16, 32, 64]))
            lrc.append(t)
            resWrite.writerow([len(data)]+t)

    with open("results/crc.csv", "w") as res:
        resWrite = csv.writer(res)
        crc_meta = ["1011", "1101111",
                    "100110001", "1100010110011001"]
        resWrite.writerow(["bits"]+crc_meta)
        for data in d:
            print(len(data))
            t = list(map(lambda b: str(crc_verify(data, b)[0]), [
                     "1011", "1101111", "100110001", "1100010110011001"]))
            crc.append(t)
            resWrite.writerow([len(data)]+t)

    with open("results/vrc.csv", "w") as res:
        resWrite = csv.writer(res)
        vrc_meta = ["Even", "Odd"]
        resWrite.writerow(["bits"]+vrc_meta)
        for data in d:
            print(len(data))
            t = list(
                map(lambda b: str(vrc_verify(data, b)[0]), [8, 16, 32, 64]))
            vrc.append(t)
            resWrite.writerow([len(data)]+t)

    x = list(map(lambda x: len(x), d))

    print("Plotting now.....")

    plot("lrc", lrc, lrc_meta, x)
    plot("cks", cks, cks_meta, x)
    plot("vrc", vrc, vrc_meta, x)
    plot("crc", crc, crc_meta, x)

    plot("overall", [[avg(lrc[i]), avg(cks[i]), avg(vrc[i]), avg(crc[i])]
         for i in range(len(x[:4]))], ["LRC", "Checksum", "VRC", "CRC"], x[:4])

    plot("overall-nocrc", [[avg(lrc[i]), avg(cks[i]), avg(vrc[i])]
         for i in range(len(x))], ["LRC", "Checksum", "VRC"], x)

    pie_plot()
