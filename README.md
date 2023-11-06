# homelab-organizer
Web app for organizing stuff in your homelab. Slow progress, primary focus is still [Webshop Scraper](https://gitlab.com/Kagee/webshop-order-scraper) for input data.

This project used to contain [Webshop Scraper](https://gitlab.com/Kagee/webshop-order-scraper) before the code became to big.

## Requirements

Python 3.9 or later. Should support  Linux/Mac OS X/Windows.

## Linux 101
````python
cd /some/folder
git clone https://gitlab.com/Kagee/homelab-organizer
cd homelab-organizer
cp example.env .env
nano .env # Edit .env to your liking
python update.py
````

## Windows 101
````bash
cd /some/folder
git clone https://gitlab.com/Kagee/homelab-organizer # or Github Desktop/other
cd homelab-organizer
cp example.env .env
notepad .env # Edit .env to your liking
python update.py
````

## (Possibly outdated) model graph
![HLO Model Graph](hlo_model_graph.png)

## Some of the external packages used

* __Haystack__ provides modular search for Django - haystack
  * <https://django-haystack.readthedocs.io/>
* __Whoosh__ search and indexing - used by Haystack
  * <https://whoosh.readthedocs.io>
* __Django REST framework__ is a powerful and flexible toolkit for building Web APIs - rest_framework
  * <https://www.django-rest-framework.org/>
* __Django-filter__ allows users to filter down a queryset based on a
  model’s fields and displaying the form to let them do this - django_filters
  * <https://django-filter.readthedocs.io>
* django_extensions
* rangefilter
* taggit
* django_bootstrap5
* Easy Bootstrap Material Design icons - django_bootstrap_icons
  * <https://github.com/christianwgd/django-bootstrap-icons>
    * <https://icons.getbootstrap.com/>
    * <https://fonts.google.com/icons>
* pygraphviz
  * <https://pygraphviz.github.io/documentation/stable/install.html#windows>


## Acknowledgements

For steadfast bug fixing, having orders that totally scramble my scraping, and coming up with those excellent ideas when I have been struggling with a bug for an hour.
<table>
<tr><td>

[![neslekkim](https://github.com/neslekkim.png/?size=50)  
neslekkim](https://github.com/neslekkim)
</td>
<td>

[![rkarlsba](https://github.com/rkarlsba.png/?size=50)  
rkarlsba](https://github.com/rkarlsba)
</td></tr>
</table>

## Notes and ideas
* <https://rk.edu.pl/en/fulltext-search-sqlite-and-django-app/>
