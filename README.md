# comicepub
digital comic epub3 generator



### Install

```Shell
pip3 install comicepub
```



### Usage

```python
from comicepub import ComicEpub

comicepub = ComicEpub("path/to/output.epub")

comicepub.add_comic_page(cover_data, cover_ext, cover=True)
for image_data, image_ext in images:
	comicepub.add_comic_page(image_data, image_ext, cover=False)
  
comicepub.title = ("Title", "Title")
comicepub.authors = [("Author 1", "Author 1")]
comicepub.publisher = ('Comicbook', 'Comicbook')
comicepub.language = "ja"

comicepub.save()
```

