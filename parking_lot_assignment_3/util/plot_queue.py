'''
Plot queue occupancy over time
'''

from helper import *

parser = argparse.ArgumentParser()
parser.add_argument('--files', '-f',
                    help="Queue timeseries output to one plot",
                    required=True,
                    action="store",
                    nargs='+',
                    dest="files")

parser.add_argument('--legend', '-l',
                    help="Legend to use if there are multiple plots.  File names used as default.",
                    action="store",
                    nargs="+",
                    default=None,
                    dest="legend")

parser.add_argument('--out', '-o',
                    help="Output png file for the plot.",
                    default=None, # Will show the plot
                    dest="out")

parser.add_argument('-s', '--summarise',
                    help="Summarise the time series plot (boxplot).  First 10 and last 10 values are ignored.",
                    default=False,
                    dest="summarise",
                    action="store_true")

parser.add_argument('--labels',
                    help="Labels for x-axis if summarising; defaults to file names",
                    required=False,
                    default=[],
                    nargs="+",
                    dest="labels")

args = parser.parse_args()
if args.labels is None:
    args.labels = args.files

to_plot=[]
for f in args.files:
    data = read_list(f)
    xaxis = map(float, col(0, data))
    start_time = xaxis[0]
    xaxis = map(lambda x: x - start_time, xaxis)
    qlens = map(float, col(1, data))
    if args.summarise:
        to_plot.append(qlens[10:-10])
    else:
        plt.plot(xaxis, qlens)

plt.title("Queue sizes")
plt.ylabel("Packets")
plt.grid()
yaxis = range(0, 1101, 50)
ylabels = map(lambda y: str(y) if y%100==0 else '', yaxis)
plt.yticks(yaxis, ylabels)
plt.ylim((0,1100))

if args.summarise:
    plt.xlabel("Link Rates")
    plt.boxplot(to_plot)
    xaxis = range(1, 1+len(args.files))
    plt.xticks(xaxis, args.labels)
    for x in xaxis:
        y = pc99(to_plot[x-1])
        print x, y
        if x == 1:
            s = '99pc: %d' % y
            offset = (-20,20)
        else:
            s = str(y)
            offset = (-10, 20)
        plt.annotate(s, (x,y+1), xycoords='data',
                xytext=offset, textcoords='offset points',
                arrowprops=dict(arrowstyle="->"))

if not args.summarise:
    plt.xlabel("Seconds")
    if args.legend:
        plt.legend(args.legend)
    else:
        plt.legend(args.files)

if args.out:
    plt.savefig(args.out)
else:
    plt.show()
