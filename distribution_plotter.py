import numpy as np
import matplotlib.pyplot as plt

import distribution_calculator as dc


def horizontal_plot():
    n = 20
    perc = dc.calculate_percentage_on_file('../type_distribution_final_cw_1')
    bins = [x[0] for x in perc][:n]
    percentages = [x[1] * 100 for x in perc][:n]
    values = [x[2] for x in perc][:n]

    pos = np.arange(len(values)) + .5  # the bar centers on the y axis

    fig = plt.figure(1)
    plt.barh(pos, percentages, align='center')
    plt.yticks(pos, bins)

    plt.title('ClueWeb Types')
    plt.xlabel('% Occurrences')
    plt.ylabel('Type')

    # plt.ylim(0, 25)

    plt.grid(True)

    ax = plt.gca()
    ax.invert_yaxis()

    # ax1 = fig.add_subplot(111)
    # ax2 = ax1.twiny()
    # ax2.xaxis.set_ticks_position("bottom")
    # ax2.xaxis.set_label_position("bottom")
    # ax2.spines["bottom"].set_position(("axes", -0.15))
    # ax2.plot(percentages)
    # ax2.set_xticks(pos)
    # values_text = [round(x/1000000, 1) for x in values][:n]
    # values_text = reversed(values_text)
    # ax2.set_xticklabels(values_text)
    # ax2.set_xlabel("# Occurrences (milions)")

    plt.tight_layout()

    # plt.show()

    plt.savefig('data/cw-types.png', bbox_inches='tight')


def vertical_plot():
    perc = dc.calculate_percentage_on_file('../type_distribution_final_cw_1')
    values = [x[2] for x in perc]
    bins = [x[0] for x in perc]

    X = np.arange(len(values))
    # plt.hist(values, bins=10)
    plt.bar(X, values, align='center', width=0.8)
    plt.xticks(X, bins)
    ymax = max(values) + 1
    plt.ylim(0, ymax)
    plt.xlim(0, 10)
    plt.title("CW types")
    plt.xlabel("Type")
    plt.ylabel("Occurrences")
    plt.show()


horizontal_plot()
