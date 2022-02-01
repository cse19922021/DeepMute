## DeepMute: Automated Mutation Testing Engine for ML Libraries.

DeepMute is a part of the project "Characterizing and Understanding Software Security Vulnerabilities in Machine Learning libraries" (see project's detail at [Link](https://cse19922021.github.io/Deep-Learning-Security-Vulnerabilities/)). DeepMute is designed to perform mutation testing on ML libraries. This version of DeepMute is preliminary and only covers Tensorflow. In future versions, we plan to extend it to the ML libraries. To run DeepMute on Tensorflow, you have to run the following commands:

## Step 1:
The first step is to run `gen_cpg.py`. There are two addresses in this script. `target_path` and `source_files_in_one_place`. You have to set these addresses with your desired address anywhere in your os. Please do not remove `sut` from the addresses. 

## Step 2:
You need to run `analyze.py` to generate a mutation database in this step. Once you run the script, you will see the mutation database is generated in your root directory as `mutation_database.db`

## Step 3: 
You need to run `get_tests_list.py` to get all available Tensorflow kernel module test files. Please modify `target_path` in this script to the directory where you have downloaded or cloned TensorFlow source files. 

## Step 4:
In this step, you need to cd to the TensorFlow source directory and configure TensorFlow with its optional parameters. You need to run ./configure.py

## Step 5:
Run `mutate.py` to start the main phase of mutation analysis. 

