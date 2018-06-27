# Moodle Archiver

*WORK IN PROGRSS*

Hey, college was neat. But now it has come to an end.

Before you loose access to Moodle, make sure all your resources are downloaded neatly for future referecnes! You could go through and download everything by hand, but this program will make the process quick & easy. Hooray!

![moodle](images/logo-small.png)

## Instructions

### Installation

With Anaconda/Miniconda:

```bash
# create conda environment, called scrapy
conda create -n scrapy python=3.6

# activate it
source activate scrapy

# install scrapy
conda install -c conda-forge scrapy
```

### Usage

```bash
# cd into first scraper directory
cd scraper

# run scrapy crawler
scrapy crawl moodle -o output/moodle.json
```

## Dev Notes

From scraper directory, local scraping via:

```bash
scrapy shell ./output/html/course-Algorithms.html
```
