#!/usr/bin/env sh

cd classification_algorithm/test
python test_continuous_transformer.py

cd ../../raspberry/
python setup.py test