# Moodle Archiver

Archive your moodle! Hooray!

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
scrapy crawl login
```