#!/bin/bash

cd /home/mastoquote/mastoquote/

sed -i 's/ignore_test_toot: False/ignore_test_toot: True/g' config.yaml
sed -i 's/disable_post: True/disable_post: False/g' config.yaml
sed -i 's/disable_dismiss: True/disable_dismiss: False/g' config.yaml
sed -i 's/loglevel: 10/loglevel: 20/g' config.yaml