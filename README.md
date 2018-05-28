# Moodle Scraper

Archive your moodle! Hooray!

## Instructions

### Installing

With Anaconda/Miniconda:

```bash
# create conda environment
conda create -n scrapy python=3.6

# install scrapy
conda install -c conda-forge scrapy

# (optional) install Jupyter
conda install jupyter
```

### Running

```bash
cd scraper
scrapy crawl login
```