#!/usr/bin/env python

import argparse
import os
import shutil
from ruamel.yaml import YAML


def parse_yaml(yaml_file):
    yaml = YAML()
    with open(yaml_file, "r") as f:
        return yaml.load(f)


def update_config(yaml_file_old, yaml_file_new, yaml_content, remove=True):
    yaml = YAML()
    yaml.default_flow_style = False
    if remove:
        os.remove(yaml_file_old)
    with open(yaml_file_new, "w") as f:
        yaml.dump(yaml_content, f)


class metaconfig:
    """
    config project directory
    """

    sub_dirs = [
        "assay",
        "results",
        "logs"
    ]

    def __init__(self, work_dir):
        self.work_dir = os.path.realpath(work_dir)
        self.metapi_dir = os.path.dirname(os.path.abspath(__file__))

        self.config_file = os.path.join(self.metapi_dir, "config", "config.yaml")
        self.cluster_file = os.path.join(self.metapi_dir, "config", "cluster.yaml")
        self.snake_file = os.path.join(self.metapi_dir, "Snakefile")

        self.new_config_file = os.path.join(self.work_dir, "config.yaml")
        self.new_cluster_file = os.path.join(self.work_dir, "cluster.yaml")

    def __str__(self):
        message = """
______             ___                         _     _
| ___ \           / _ \                       | |   | |
| |_/ / __ _  ___/ /_\ \___ ___  ___ _ __ ___ | |__ | |_   _
| ___ \/ _` |/ __|  _  / __/ __|/ _ \ '_ ` _ \| '_ \| | | | |
| |_/ / (_| | (__| | | \__ \__ \  __/ | | | | | |_) | | |_| |
\____/ \__,_|\___\_| |_/___/___/\___|_| |_| |_|_.__/|_|\__, |
                                                        __/ |
                                                       |___/

           Omics for All, Open Source for All

    Hybrid assembly and polish using short and long reads


A projects have been created on %s

Thanks for using BacAssembly.


Now, you can use "bacassembly denovo_wf":

        bacassembly denovo_wf --list

        bacassembly denovo_wf --run

        bacassembly denovo_wf --run --use_conda

        bacassembly denovo_wf --debug

        bacassembly denovo_wf --dry_run

        bacassembly denovo_wf --qsub

        bacassembly denovo_wf --qsub --use_conda
""" % self.work_dir

        return message

    def create_dirs(self):
        """
        create project directory
        """
        if not os.path.exists(self.work_dir):
            os.mkdir(self.work_dir)

        for sub_dir in metaconfig.sub_dirs:
            os.makedirs(os.path.join(self.work_dir, sub_dir), exist_ok=True)

    def get_config(self):
        """
        get default configuration
        """
        config = parse_yaml(self.config_file)
        cluster = parse_yaml(self.cluster_file)
        config["snakefile"] = self.snake_file
        config["configfile"] = self.new_config_file
        config["clusterfile"] = self.new_cluster_file
        return (config, cluster)
