#!/usr/bin/env python3

import requests
import matplotlib.pyplot as plt


def main():
    # Please convert cson files into json first
    # Use requests to avoid boring Windows encoding problem
    mapspot = requests.get('http://127.0.0.1:8000/mapspot.json').json()
    maproute = requests.get('http://127.0.0.1:8000/maproute.json').json()

    for section_key, section in mapspot.items():
        for map_key, map in section.items():
            print("Draw spot %s-%s" % (section_key, map_key))
            plt.clf()
            # fig, ax = plt.subplots()
            # ax.xaxis.set_ticks_position('top')
            plt.xlim(0, 15000)
            plt.ylim(8000, 0)
            ns = []
            xs = []
            ys = []
            for n, v in map.items():
                ns.append(int(n))
                xs.append(v[0])
                ys.append(v[1])
            plt.scatter(xs, ys, s=100)
            for n, x, y in zip(ns, xs, ys):
                plt.annotate(
                    n, xy=(x, y), xytext=(x + 100, y + 100),
                    # textcoords='offset points',
                    # bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                    # arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
                    )
            plt.title("%s - %s" % (section_key, map_key))
            plt.savefig("spot-%s_%s.png" % (section_key, map_key),
                        dpi=150, format="png")

    for section_key, section in mapspot.items():
        for map_key, map in section.items():
            print("Draw route %s-%s" % (section_key, map_key))
            plt.clf()
            ns = []
            xs = []
            ys = []
            for k, v in map.items():
                ns.append(k)
                xs.append(v[0])
                ys.append(-v[1])
            plt.scatter(xs, ys, s=100)
            plt.xlim(0, 15000)
            plt.ylim(-8000, 0)

            if section_key not in maproute:
                continue
            if map_key not in maproute[section_key]:
                continue

            for route in maproute[section_key][map_key]:
                x1, y1 = map[str(route[0])]
                x2, y2 = map[str(route[1])]

                print([x1, x2], [-y1, -y2],)
                plt.plot([x1, x2], [-y1, -y2], 'k-')
            plt.title("%s - %s" % (section_key, map_key))
            plt.savefig("route-%s_%s.png" % (section_key, map_key),
                        dpi=150, format="png")

    plt.close()


if __name__ == '__main__':
    main()
