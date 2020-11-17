# QartNewSurfer
Silver Surfer of Qartvelian Web Media

## Dependencies

```shell script
pip install -r requirements.txt
```

## Instruction
navigate to the QartNewSurfer toolset directory:
 ```shell script
cd qartnewsurfer
```

and run the desired surfer:
 ```shell script
scrapy crawl <surf_board>
```

## List of current NewSurfers

surf_board | surfer
--- | ---
onge | on.ge 

## Attributes
full shell command example with attributes:

```shell script
scrapy crawl onge -a category=1 start_page=2 max_page=5
```

### Table of Attributes
attribute | description | example
--- | --- | ---
category | post category in int (check the categories for the surfboard)| `category=2`
start_page | page index to start scrapping from (default=0)| `start_page=50`
max_page | page index to end scrapping at (default is the last "next" page for the platform) | `max_page=110`

### Storing the scraped data
```shell script
scrapy crawl onge -O pages.json
```
That will generate an quotes.json file containing all scraped items, serialized in JSON.

When appending to a file, consider using a different serialization format, such as JSON Lines:
```shell script
scrapy crawl onge -o pages.jl
```
scrapy crawl onge -O quotes-humor.json -a category=1 -a start_page=2 -a max_page=5
