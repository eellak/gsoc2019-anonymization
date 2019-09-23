#!/usr/bin/env bash
echo 'Copying files to src/anonymizer_service/ ...'
cp -r ./anonymizer/* ./src/anonymizer_service/
echo 'Updating relative imports ...'
sed -E 's/from anonymizer/from anonymizer_service/' anonymizer/__init__.py > src/anonymizer_service/__init__.py
sed -E 's/from anonymizer/from anonymizer_service/' anonymizer/__main__.py > src/anonymizer_service/__main__.py
sed -E 's/from anonymizer/from anonymizer_service/' anonymizer/anonymize.py > src/anonymizer_service/anonymize.py
sed -E 's/from anonymizer/from anonymizer_service/' anonymizer/external_functions.py > src/anonymizer_service/external_functions.py
sed -E 's/from anonymizer/from anonymizer_service/' anonymizer/matcher_patterns.py > src/anonymizer_service/matcher_patterns.py 
sed -E 's/from anonymizer/from anonymizer_service/' anonymizer/trie_index.py > src/anonymizer_service/trie_index.py
echo 'Service updated ...'
