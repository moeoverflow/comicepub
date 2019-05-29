import os.path
import zipfile
import uuid
import datetime
from typing import Tuple, List, Set
from mimetypes import MimeTypes
from .render import render_mimetype
from .render import render_container_xml
from .render import render_navigation_documents_xhtml
from .render import render_standard_opf
from .render import render_xhtml
from .render import get_fixed_layout_jp_css


class ComicEpub:
    """
    This ComicEpub class is dedicated to generating ditigal comic EPUB files conataining image-only content.
    """

    def __init__(
            self, filename,
            epubid: str = uuid.uuid1(),
            title: Tuple[str, str] = None,
            subjects: Set[str] = None,
            authors: List[Tuple[str, str, str]] = None,
            publisher: Tuple[str, str] = None,
            language: str = "ja",
            updated_date: str = datetime.datetime.now().isoformat(),
            view_width: int = 848,
            view_height: int = 1200,
    ):
        """
        Create a zip file as an EPUB container, which is only epub-valid after calling the save() method.

        :rtype: instance of ComicEpub
        :param filename: epub file path to save
        :param epubid: unique epub id - Default: random uuid
        :param title: epub title - Tuple(title, file_as) - Default: Unknown Title
        :param authors: epub authors - List of Tuple(author_name, file_as) - Default: Unknown Author
        :param publisher: epub publisher - Tuple(publisher_name, file_as) - Default: Unknown Publisher
        :param language: epub language - Default: ja
        :param updated_date: epub updated_date - Default: current time
        :param view_width: epub view_width - Default: 848
        :param view_height: epub view_height - Default: 1200
        """
        if title is None:
            self.title = ('Unknown Title', 'Unknown Title')
        else:
            self.title = title
        if subjects is None:
            self.subjects = set()
        else:
            self.subjects = subjects
        if authors is None:
            self.authors = [('Unknown Author', 'Unknown Author')]
        else:
            self.authors = authors
        if publisher is None:
            self.publisher = ('Unknown Publisher', 'Unknown Publisher')
        else:
            self.publisher = publisher

        self.epubid = epubid
        self.authors = authors
        self.publisher = publisher
        self.language = language
        self.updated_date = updated_date
        self.view_width = view_width
        self.view_height = view_height

        self.manifest_images: List[Tuple[str, str, str]] = []
        self.manifest_xhtmls: List[Tuple[str, str]] = []
        self.manifest_spines: List[str] = []

        self.nav_title = "Navigation"
        self.nav_items: List[Tuple[str, str]] = []

        self.epub = None
        self.__open(filename)

        self.mime = MimeTypes()

    def __open(self, filename):

        if '.epub' not in filename:
            filename += '.epub'

        full_file_name = os.path.expanduser(filename)
        path = os.path.split(full_file_name)[0]
        if not os.path.exists(path):
            os.makedirs(path)
        self.epub = zipfile.ZipFile(full_file_name, 'w')

    def __close(self):
        self.epub.close()

    def __add_image(self, index: int, image_data, image_ext, cover: bool = False):
        if cover:
            image_id = "cover"
        else:
            image_id = "i-" + "%04d" % index

        path = "item/image/" + image_id + image_ext
        self.epub.writestr(path, image_data)

        mimetype = self.mime.guess_type('test' + image_ext)
        if mimetype[0] is None:
            image_mimetype = "image/jpeg"
        else:
            image_mimetype = mimetype[0]
        return image_id, image_ext, image_mimetype

    def __add_xhtml(self, index: int, title: str, image_id: str, image_ext: str, cover: bool = False):
        if cover:
            xhtml_id = "p-cover"
        else:
            xhtml_id = "p-" + "%04d" % index

        content = render_xhtml(title, image_id, image_ext, self.view_width, self.view_height, cover)
        self.epub.writestr("item/xhtml/" + xhtml_id + ".xhtml", content)
        return xhtml_id

    def add_comic_page(self, image_data, image_ext, cover=False):
        """
        Add images to the page in order, each image is a page.

        :param image_data: data of image
        :param image_ext: extension of image
        :param cover: true if image is cover
        """
        index = len(self.manifest_xhtmls)
        image_id, image_ext, image_mimetype = self.__add_image(index, image_data, image_ext, cover)
        xhtml_id = self.__add_xhtml(index, self.title[0], image_id, image_ext, cover)

        self.manifest_images.append((image_id, image_ext, image_mimetype))
        self.manifest_xhtmls.append((xhtml_id, image_id))
        self.manifest_spines.append(xhtml_id)

    def save(self):
        """
        generate epub required files, then close and save epub file.
        """
        self.epub.writestr("mimetype", render_mimetype())
        self.epub.writestr("META-INF/container.xml", render_container_xml())
        self.epub.writestr("item/standard.opf", render_standard_opf(
            uuid=self.epubid,
            title=self.title,
            subjects=self.subjects,
            authors=self.authors,
            publisher=self.publisher,
            language=self.language,
            updated_date=self.updated_date,
            view_width=self.view_width,
            view_height=self.view_height,
            manifest_images=self.manifest_images,
            manifest_xhtmls=self.manifest_xhtmls,
            manifest_spines=self.manifest_spines,
        ))
        self.nav_items.append(('p-cover', 'Cover'))
        self.epub.writestr("item/navigation-documents.xhtml", render_navigation_documents_xhtml(
            title=self.nav_title,
            nav_items=self.nav_items,
        ))
        self.epub.writestr("item/style/fixed-layout-jp.css", get_fixed_layout_jp_css())

        self.__close()
