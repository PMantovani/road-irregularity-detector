#!/usr/bin/env sh

cd classification_algorithm/test
python test_continuous_transformer.py

cd ../../raspberry/test
python i2cdevice_test.py