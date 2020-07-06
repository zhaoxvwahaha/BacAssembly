#!/usr/bin/env python

import os
import sys
import pandas as pd


def parse_samples(config):
    samples_df = pd.read_csv(config["params"]["samples"], sep="\s+").set_index(
        "id", drop=False
    )
    cancel = False
    for sample_id in samples_df.index.unique():
        lq_list = samples_df.loc[[sample_id], "long_reads"].dropna().tolist()
        sq1_list = samples_df.loc[[sample_id], "short_reads_1"].dropna().tolist()
        sq2_list = samples_df.loc[[sample_id], "short_reads_2"].dropna().tolist()

        for fq_file in lq_list + sq1_list + sq2_list:
            if not fq_file.endswith(".gz"):
                print("%s need gzip format" % fq_file)
                cancel = True
            if not os.path.exists(fq_file):
                print("%s not exists" % fq_file)
                cancel = True

    if cancel:
        sys.exit(-1)
    else:
        return samples_df


def get_reads(sample_df, wildcards, col):
    return sample_df.loc[[wildcards.sample], col].dropna().tolist()


def get_sample_id(sample_df, wildcards, col):
    return sample_df.loc[wildcards.sample, [col]].dropna()[0]
