#!/bin/bash

FILENAME="data.txt"
COUNT=10000

> $FILENAME

echo "Generating $COUNT bits in $FILENAME..."

for ((i=1; i<=COUNT; i++))
do
    echo -n $(( $RANDOM % 2 )) >> $FILENAME
done

echo "Done!"