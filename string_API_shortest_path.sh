#!/bin/bash

# Latest download: https://string-db.org/cgi/download?sessionId=bIJIOttT3oi6
wget https://stringdb-static.org/download/protein.physical.links.v11.5/9606.protein.physical.links.v11.5.txt.gz
gunzip 9606.protein.physical.links.v11.5.txt.gz
python3.9 string_API_shortest_path.py 9606.protein.physical.links.v11.5.txt $1 $2
rm -rf 9606.protein.physical.links.v11.5.txt
