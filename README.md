# comicepub
digital comic epub3 generator



### Install

```Shell
pip3 install comicepub
```



### Usage

```shell
comicepub --help
usage: comicepub [-h] -t TITLE --author AUTHOR [--publisher PUBLISHER] [--language LANGUAGE] -i INPUT -o OUTPUT
                 [--cover COVER] [--version]

optional arguments:
  -h, --help            show this help message and exit
  -t TITLE, --title TITLE
                        Book title
  --author AUTHOR       Book author
  --publisher PUBLISHER
                        Book publisher
  --language LANGUAGE   Book language
  -i INPUT, --input INPUT
                        Source images directory of comic book
  -o OUTPUT, --output OUTPUT
                        Output filename of comic book
  --cover COVER         cover image file of comic book
  --version             show program's version number and exit
```

```shell
comicepub \
  -i /path/to/your/comicdir \
  -o /path/to/save/output.epub \
  --title "Comicbook" \
  --author "comicepub" \
  --language "zh"
```

```python
from comicepub import ComicEpub

comicepub = ComicEpub("path/to/output.epub")

comicepub.title = ("Title", "Title")
comicepub.authors = [("Author 1", "Author 1")]
comicepub.publisher = ('Comicbook', 'Comicbook')
comicepub.language = "ja"

comicepub.add_comic_page(cover_data, cover_ext, cover=True)
for image_data, image_ext in images:
	comicepub.add_comic_page(image_data, image_ext, cover=False)

comicepub.save()
```

