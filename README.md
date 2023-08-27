# homelab-organizer
Web app for organizing stuff in your homelab. Slow progress, primary focus is still [Webshop Scraper](https://gitlab.com/Kagee/webshop-order-scraper) for input data.

This project used to contain [Webshop Scraper](https://gitlab.com/Kagee/webshop-scraper) before the code became to big.

## Requirements

Python 3.9 or later. Should support  Linux/Mac OS X/Windows.

## Linux 101
````python
cd /some/folder
git clone https://gitlab.com/Kagee/homelab-organizer.git
cd homelab-organizer
cp example.env .env
nano .env # Edit .env to your liking
python update.py
````

## Windows 101
````bash
cd /some/folder
git clone https://gitlab.com/Kagee/homelab-organizer.git # or Github Desktop/other
cd homelab-organizer
cp example.env .env
notepad .env # Edit .env to your liking
python update.py
````

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
