#!/usr/bin/env python

"""
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

"""

import argparse
import os
import sys
import subprocess
import textwrap

import bacassembly


WORKFLOWS = [
    "trimming_all",
    "all"
]


def init(args):
    if args.workdir:
        project = bacassembly.metaconfig(args.workdir)
        print(project.__str__())
        project.create_dirs()
        conf, cluster = project.get_config()

        if args.begin:
            conf["params"]["begin"] = args.begin
            if args.begin == "rmhost":
                conf["params"]["trimming"]["fastp"]["do"] = False
                conf["params"]["rmhost"]["bowtie2"]["do"] = True
            elif args.begin == "assembly":
                conf["params"]["trimming"]["fastp"]["do"] = False
                conf["params"]["rmhost"]["bowtie2"]["do"] = False

        if args.samples:
            conf["params"]["samples"] = args.samples

        bacassembly.update_config(
            project.config_file, project.new_config_file, conf, remove=False
        )
        bacassembly.update_config(
            project.cluster_file, project.new_cluster_file, cluster, remove=False
        )
    else:
        print("Please supply a workdir!")
        sys.exit(1)


def denovo_wf(args):
    config_file = os.path.join(args.workdir, "config.yaml")
    conf = bacassembly.parse_yaml(config_file)

    if not os.path.exists(conf["params"]["samples"]):
        print("Please specific samples list on init step or change config.yaml manualy")
        sys.exit(1)

    cmd = [
        "snakemake",
        "--snakefile",
        conf["snakefile"],
        "--configfile",
        args.config,
        "--cores",
        str(args.cores),
        "--rerun-incomplete",
        "--keep-going",
        "--printshellcmds",
        "--reason",
        "--until",
        args.task
    ]

    if args.list:
        cmd += ["--list"]
    elif args.run:
        cmd += [""]
    elif args.debug:
        cmd += ["--debug-dag", "--dry-run"]
    elif args.dry_run:
        cmd += ["--dry-run"]
    elif args.qsub:
        cmd += [
            "--cluster-config",
            conf["clusterfile"],
            "--jobs",
            str(args.jobs),
            "--latency-wait",
            str(args.wait),
            '--cluster "qsub -S /bin/bash -cwd \
            -q {cluster.queue} -P {cluster.project} \
            -l vf={cluster.mem},p={cluster.cores} \
            -binding linear:{cluster.cores} \
            -o {cluster.output} -e {cluster.error}"',
        ]

    if not args.snake is None:
        cmd += ["--" + args.snake]

    cmd_str = " ".join(cmd).strip()
    print("Running bacassembly denovo_wf:\n%s" % cmd_str)

    env = os.environ.copy()
    proc = subprocess.Popen(
        cmd_str, shell=True, stdout=sys.stdout, stderr=sys.stderr, env=env,
    )
    proc.communicate()


def main():
    banner = """
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

"""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(banner),
        prog="bacassembly",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        default=False,
        help="print software version and exit",
    )

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        "-d",
        "--workdir",
        metavar="WORKDIR",
        type=str,
        default="./",
        help="project workdir, default: ./",
    )

    subparsers = parser.add_subparsers(title="available subcommands", metavar="")
    parser_init = subparsers.add_parser(
        "init",
        parents=[parent_parser],
        prog="bacassembly init",
        help="init project",
    )
    parser_denovo_wf = subparsers.add_parser(
        "denovo_wf",
        parents=[parent_parser],
        prog="bacassembly denovo_wf",
        help="denovo_wf pipeline",
    )

    parser_init.add_argument(
        "-s",
        "--samples",
        type=str,
        default=None,
        help="""desired input:
samples list, tsv format required.
        header: ["id", "long_reads", "short_reads_1", "short_reads_2"]
"""
    )
    parser_init.add_argument(
        "-b",
        "--begin",
        type=str,
        default="trimming",
        choices=["trimming", "rmhost", "assembly"],
        help="pipeline starting point",
    )
    parser_init.set_defaults(func=init)

    parser_denovo_wf.add_argument(
        "task",
        metavar="TASK",
        nargs="?",
        type=str,
        default="all",
        choices=WORKFLOWS,
        help="pipeline end point. Allowed values are " + ", ".join(WORKFLOWS),
    )
    parser_denovo_wf.add_argument(
        "--config",
        type=str,
        default="./config.yaml",
        help="config.yaml, default: ./config.yaml",
    )
    parser_denovo_wf.add_argument(
        "--cores", type=int, default=8, help="CPU cores, default: 8"
    )
    parser_denovo_wf.add_argument(
        "--jobs", type=int, default=80, help="qsub job numbers, default: 80"
    )
    parser_denovo_wf.add_argument(
        "--list", default=False, action="store_true", help="list pipeline rules",
    )
    parser_denovo_wf.add_argument(
        "--run", default=False, action="store_true", help="run pipeline",
    )
    parser_denovo_wf.add_argument(
        "--debug", default=False, action="store_true", help="debug pipeline",
    )
    parser_denovo_wf.add_argument(
        "--dry_run", default=False, action="store_true", help="dry run pipeline",
    )
    parser_denovo_wf.add_argument(
        "--qsub", default=False, action="store_true", help="qsub pipeline",
    )
    parser_denovo_wf.add_argument(
        "--wait", type=int, default=60, help="wait given seconds, default: 60"
    )
    parser_denovo_wf.add_argument(
        "--snake",
        metavar="SNAKEMAKEARGS",
        nargs="?",
        type=str,
        default=None,
        help="other snakemake command options(sankemake -h), if want --touch, just --snake touch",
    )
    parser_denovo_wf.set_defaults(func=denovo_wf)

    args = parser.parse_args()
    try:
        if args.version:
            print("bacassembly version %s" % bacassembly.__version__)
            sys.exit(0)
        args.func(args)
    except AttributeError as e:
        print(e)
        parser.print_help()


if __name__ == "__main__":
    main()
