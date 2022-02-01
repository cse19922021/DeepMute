#!/bin/bash

cd /home/nimashiri/tmp/tensorflow_pkg

pip3 uninstall --yes tensorflow

pip3 install tensorflow-2.7.0-cp38-cp38-linux_x86_64.whl

sudo rm -rf tensorflow-2.7.0-cp38-cp38-linux_x86_64.whl






