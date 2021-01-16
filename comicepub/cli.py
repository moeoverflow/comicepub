import argparse
import os
from comicepub import ComicEpub
from comicepub.version import __version__


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--title", help=u"Book title", required=True)
    parser.add_argument("--author", help=u"Book author", required=True)
    parser.add_argument("--publisher", help=u"Book publisher")
    parser.add_argument("--language", help=u"Book language")

    parser.add_argument("-i", "--input", help=u"Source images directory of comic book", required=True)
    parser.add_argument("-o", "--output", help=u"Output filename of comic book", required=True)
    parser.add_argument("--cover", help=u"cover image file of comic book")

    parser.add_argument('--version', action='version', version="%(prog)s {version}".format(version=__version__))

    return parser.parse_args()


def generate_epub(args):
    comicepub = ComicEpub(args.output)

    comicepub.title = (args.title, args.title)
    comicepub.authors = [(args.author, args.author)]
    if args.publisher is not None:
        comicepub.publisher = (args.publisher, args.publisher)
    if args.language is not None:
        comicepub.language = args.language

    images = os.listdir(args.input)
    images.sort()

    for index, image in enumerate(images):
        is_cover = index == 0
        with open(os.path.join(args.input, image), 'rb') as file:
            data = file.read()
            ext = os.path.splitext(image)[1]
            comicepub.add_comic_page(data, ext, cover=is_cover)

    comicepub.save()


def main():
    args = parse_args()
    generate_epub(args)


if __name__ == '__main__':
    main()
