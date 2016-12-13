import pprint
from lib.util.image_analysis import get_color_count, get_color_classes
from lib import model


def get_parser():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--input",
                        dest="input",
                        help="read this file",
                        metavar="FILE",
                        required=True)
    return parser


if __name__ == "__main__":

    args = get_parser().parse_args()

    color_classes = get_color_classes(args.input, [
        ("red", (255, 0, 0)),
        ("green", (0, 255, 0)),
        ("blue", (0, 0, 255)),
        ("white", (255, 255, 255)),
        ("black", (0, 0, 0))
    ], threshold=130)

    area_analysis = model.AreaAnalysis(
        color_classes["red"]["count"],
        color_classes["green"]["count"],
        color_classes["blue"]["count"],
        color_classes["white"]["count"],
        color_classes["black"]["count"],
        color_classes["unknown"]["count"])

    print("*** color analysis result ***")
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(color_classes)

    print("*** area analysis result ***")
    print(area_analysis)
