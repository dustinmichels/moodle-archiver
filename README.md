# Moodle Archiver

Download a local copy of your Moodle files and pages. Hooray!

*WORK IN PROGRSS*

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
scrapy crawl moodle -o moodle.json
```

## Dev

```bash
scrapy shell ./html/course-Algorithms.html
```