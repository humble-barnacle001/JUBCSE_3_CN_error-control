import matplotlib.pyplot as plt

from application.cks import cks_verify
from application.lrc import lrc_verify
from application.vrc import vrc_verify
from application.crc import crc_verify


def pie_plot():
    ct = [0, 0, 0, 0]
    label = ["vrc", "lrc", "crc", "cks"]
    r = 16

    for i in range(2**r):
        x = bin(i)[2:]
        x = ("0"*(r-len(x)))+x
        if(x != "1010100101000111"):
            d = x+"0"
            if(vrc_verify(d, "Even")[1]):
                ct[0] += 1
            d = x+"00"
            if(lrc_verify(d, 2)[1]):
                ct[1] += 1
            d = x+"011"
            if(crc_verify(d, "1011")[1]):
                ct[2] += 1
            d = x+"1101"
            if(cks_verify(d, 4)[1]):
                ct[3] += 1

    print("Plotting pie charts...")
    for x in range(len(ct)):
        plt.pie(
            [ct[x], 2**r-ct[x]],
            labels=[
                "Not detected = {:.2f}%".format((ct[x]/(2**r)) * 100),
                "Detected = {:.2f}%".format((1-ct[x]/(2**r)) * 100)
            ],
            startangle=270,
            wedgeprops={"edgecolor": "black",
                        'linewidth': 2,
                        'antialiased': True}
        )
        plt.title("{} error detection probability".format(label[x]))
        # plt.show()
        plt.savefig("results/pie-"+label[x]+".png", bbox_inches='tight')
        plt.clf()
    plt.bar(label, list(map(lambda x: ((x/(2**r)) * 100), ct)))
    plt.xlabel("Error control technique")
    plt.ylabel("% NOT detected")
    plt.title("Overall non-detected case probability")
    plt.savefig("results/pie-overall.png", bbox_inches='tight')
    # plt.show()
    print("Done")


if __name__ == "__main__":
    pie_plot()
