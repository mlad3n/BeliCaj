#!/bin/bash

python crawl.py https://www.reddit.com/r/blackhat/new/ https://www.reddit.com/r/security/new/ https://www.reddit.com/r/security/new/ https://www.reddit.com/r/darknet/
python topic_modeling_prep.py
open Report.twb