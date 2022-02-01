#!/bin/bash

# if you see llvm download error, you may want to run bazel clean 

cd /media/nimashiri/SSD/tensorflow

# pip3 install --user -U pip six 'numpy<1.19.0' wheel setuptools mock 'future>=0.17.1'
# pip3 install --user -U keras_applications --no-deps
# pip3 install --user -U keras_preprocessing --no-deps

# bazelisk-linux-amd64 clean --expunge

bazel --output_user_root=/media/nimashiri/SSD/bazel_temp_dir build --config=opt -c opt //tensorflow/tools/pip_package:build_pip_package --jobs=4

#/home/nimashiri/bazel-4.2.2/output/bazel --output_user_root=/media/nimashiri/SSD/bazel_temp_dir build --jobs=6 --config=opt -c fastbuild //tensorflow/tools/pip_package:build_pip_package 


