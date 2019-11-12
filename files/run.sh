#!/bin/bash
conda activate p3.6 > /dev/null 2>&1
if [ $? -ne 0 ]
then
    source activate p3.6 > /dev/null 2>&1
fi
python -m scrapy crawl $SPIDER_NAME$
conda deactivate /dev/null 2>&1
if [ $? -ne 0 ]
then
    source deactivate > /dev/null 2>&1
fi