# BacAssembly 

A hybrid assembly pipeline for bacteria

## Installation

bacassembly works with Python 3.6+.

```
[WIP]
$ conda install -c bioconda bacassembly
```

Or via pip:

```
[WIP]
$ pip install bacassembly
```

## Run

### help

```
$ bacassembly --help

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

  optional arguments:
  -h, --help     show this help message and exit
  -v, --version  print software version and exit

  available subcommands:

  init         init project
  denovo_wf    denovo_wf pipeline
```

### init

```
$ bacassembly init --help
  usage: bacassembly init [-h] [-d WORKDIR] [-s SAMPLES]
                          [-b {trimming,rmhost,assembly}]

  optional arguments:
  -h, --help            show this help message and exit
  -d WORKDIR, --workdir WORKDIR
                        project workdir, default: ./
  -s SAMPLES, --samples SAMPLES
                        desired input: samples list, tsv format required.
                        header: ["id", "long_reads", "short_reads_1", "short_reads_2"]
  -b {trimming,rmhost,assembly}, --begin {trimming,rmhost,assembly}
                        pipeline starting point

```

### denovo_wf

```
$ bacassembly denovo_wf --help
  usage: bacassembly denovo_wf [-h] [-d WORKDIR] [--config CONFIG]
                               [--cores CORES] [--jobs JOBS] [--list] [--run]
                               [--debug] [--dry_run] [--qsub] [--wait WAIT]
                               [--snake [SNAKEMAKEARGS]]
                               [TASK]

  positional arguments:
  TASK                  pipeline end point. Allowed values are trimming_all,
                        all

  optional arguments:
  -h, --help            show this help message and exit
  -d WORKDIR, --workdir WORKDIR
                        project workdir, default: ./
  --config CONFIG       config.yaml, default: ./config.yaml
  --cores CORES         CPU cores, default: 8
  --jobs JOBS           qsub job numbers, default: 80
  --list                list pipeline rules
  --run                 run pipeline
  --debug               debug pipeline
  --dry_run             dry run pipeline
  --qsub                qsub pipeline
  --wait WAIT           wait given seconds, default: 60
  --snake [SNAKEMAKEARGS]
                        other snakemake command options(sankemake -h), if want
                        --touch, just --snake touch

```

### Example

```
# init project
$ bacassembly init -d . -s samples.tsv -b trimming

# run trimming
$ metapi denovo_wf trimming_all --run

# run all
$ metapi denovo_wf --run
```

## input requirements

The input samples file: `samples.tsv` format:

Note: If `id` col contain same id, then the reads of each sample will be merged.
Note: The fastq need gzip compress.

  | id  | long_reads    | short_reads_1 | short_reads_2 |
  | :-: | :-----:       | :-----:       | :-----:       |
  | s1  | aa.long.fq.gz | aa.1.fq.gz    | aa.2.fq.gz    |
  | s2  | bb.long.fq.gz | bb.1.fq.gz    | bb.2.fq.gz    |
  | s2  | cc.long.fq.gz | cc.1.fq.gz    | cc.2.fq.gz    |
  | s3  | dd.long.fq.gz | dd.1.fq.gz    | dd.2.fq.gz    |

## Getting help

If you want to report a bug or issue, or have problems with installing or
running the software, please create [a new issue](https://github.com/zhaoxywahaha/BacAssembly/issues).

## License

This module is licensed under the terms of the [GPLv3 license](https://opensource.org/licenses/GPL-3.0).