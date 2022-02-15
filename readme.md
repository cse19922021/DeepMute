## DeepMute: Automated Mutation Testing Engine for machine learning Libraries.

DeepMute is an automated mutation testing engine for machine learning libraries. This version of DeepMute is preliminary and only covers Tensorflow. In future versions, we plan to extend it to support other libraries, including but not limited to Pandas and Numpy. DeepMute uses vulnerability patterns extracted and analyzed in our paper titled "Characterizing and Understanding Software Security Vulnerabilities in Machine Learning libraries" (see project's detail at [Link](https://cse19922021.github.io/Deep-Learning-Security-Vulnerabilities/)) to insert mutation operators. DeepMute inserts one mutation simultaneously, compiles TensorFlow against applied changes, and stores the results into its mutation database.  

## Requirements

DeepMute uses [Bazel](https://gist.github.com/kmhofmann/e368a2ebba05f807fa1a90b3bf9a1e03) build tool to compile Tensorflow library. Please follow the provided Link to install the bazel.

[SQLite3](https://docs.python.org/3/library/sqlite3.html) is the only external dependency required by DeepMute. Please use the following command to install it:
```
  $ pip install SQLite
```

## Running DeepMute
To run DeepMute, you need to run the following commands explained in each step. Please use the following command to clone DeepMute before you start running the scripts:

```
$ git clone https://github.com/cse19922021/DeepMute.git
```

### Analyze:
This is the first phase of the DeepMute process, where it analyzes all kernel source files to extract and store potential mutation. The usage is as follows:

```
  $ python analyze.py --target_path=../tensorflow/tensorflow/core/kernels/
```
```target_path``` is a directory where you have cloned TensorFlow source files from Github. Please use the following commands to clone TensorFlow:
```
  $ git clone https://github.com/tensorflow/tensorflow
  $ cd tensorflow
  $ git checkout v2.7.0
```

Please note that DeepMute works on branch ```v2.7.0```.

Once the process is finished, ```mutation_database.db``` will be generated under the root directory where you have cloned DeepMute. This file is the main building block of DeepMute, where all potential mutation is stored. 

You need to run `analyze.py` to generate a mutation database in this step. Once you run the script, you will see the mutation database is generated in your root directory as `mutation_database.db`

### Getting test files:

You need to run `get_tests_list.py` to get all available Tensorflow kernel module test files in this step. The usage is as follows:

```
$ python get_tests_list.py --target_path=../tensorflow/tensorflow/python/kernel_tests/
```

### Start mutation analysis:
In the final step, you need to run `mutate.py` with the following usage:

```
$ python mutate.py --temp_path=/random/path/to/copy/tensorflow/source/files --library_path=../tensorflow/ --tensorflow_pkg_path=/your/desired/path/tensorflow_pkg
```
The following parameters are critical to DeepMute:

```temp_path``` is a temporary path to TensorFlow source files. Please copy and paste the cloned TensorFlow source files to your desired address. You only need to do this process once. 

```library_path``` is the path to cloned TensorFlow source files. 

```tensorflow_pkg_path``` is a directory where bazel will generate a TensorFlow package for pip installation.

