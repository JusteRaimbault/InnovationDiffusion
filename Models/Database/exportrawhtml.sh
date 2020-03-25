
ID=$1

#mongoexport --db uspto --collection raw --query "{id:$ID}" -f html --type=csv -o test/$ID.html
mongoexport --db uspto --collection raw --query "{id:$ID}" -f html --type=csv -o ../../Data/exports/$ID.html.json

