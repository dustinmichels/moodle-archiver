# Moodle Archiver

*WORK IN PROGRSS*

Hey, college was neat. But now it has come to an end.

There are lots of things to be scared of, but loosing access
to Moodle and the course materials therein, is no longer one of them!

Use this program to download a local copy of your Moodle files
and pages today. Hooray!!!

![moodle](images/logo-small.png)

## Instructions

### Installation

With Anaconda/Miniconda:

```bash
# create conda environment, called moodle
conda create -n moodle python=3.6

# activate it
source activate moodle

# install scrapy
conda install -c conda-forge scrapy
```

### Usage

```bash
# cd into first scraper directory
cd scraper

# run scrapy crawler
scrapy crawl moodle -t json -o - > "output/moodle.json"
scrapy crawl moodle -o output/moodle.json
```

## Dev Notes

From scraper directory, local scraping via:

```bash
scrapy shell ./output/html/course-Algorithms.html
scrapy shell "./output/html/2017-2018/Winter '18/course-Computability and Complexity.html"
```