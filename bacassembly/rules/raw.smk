def raw_long_reads(wildcards):
    return [bacassembly.get_reads(SAMPLES, wildcards, "long_reads")]


def raw_short_reads(wildcards):
    return [bacassembly.get_reads(SAMPLES, wildcards, "short_reads_1"),
            bacassembly.get_reads(SAMPLES, wildcards, "short_reads_2")]


rule prepare_long_reads:
    input:
        unpack(raw_long_reads)
    output:
        os.path.join(
            config["output"]["raw"],
            "long_reads/{sample}/{sample}.long.raw.fq.gz")
    run:
        if len(input) == 1:
            shell('''ln -s %s {output[0]}''' % os.path.realpath(input[0]))
        else:
            shell('''cat {input} > {output[0]}''')


rule prepare_long_reads_all:
    input:
        expand(os.path.join(
            config["output"]["raw"],
            "long_reads/{sample}/{sample}.long.raw.fq.gz"),
               sample=SAMPLES.index.unique())


rule prepare_short_reads:
    input:
        unpack(raw_short_reads)
    output:
        expand(os.path.join(
            config["output"]["raw"],
            "short_reads/{{sample}}/{{sample}}.short.raw{read}.fq.gz"),
               read=[".1", ".2"])
    run:
        if len(input) == 2:
            shell('''ln -s %s {output[0]}''' % os.path.realpath(input[0]))
            shell('''ln -s %s {output[1]}''' % os.path.realpath(input[1]))
        else:
            shell('''cat %s > %s''' % (" ".join(input[0:reads_num//2]), output[0]))
            shell('''cat %s > %s''' % (" ".join(input[reads_num//2:]), output[1]))


rule prepare_short_reads_all:
    input:
        expand(os.path.join(
            config["output"]["raw"],
            "short_reads/{sample}/{sample}.short.raw{read}fq.gz"),
               read=[".1", ".2"],
               sample=SAMPLES.index.unique())


def get_reads(wildcards, long_or_short, step):
    LONG_OR_SHORT = {
        "long": "long_reads",
        "short": "short_reads"
    }
    READS = {
        "long": [""],
        "short": [".1", ".2"]
    }
    return expand(
        os.path.join(
            config["output"][step], LONG_OR_SHORT[long_or_short],
            "{sample}/{sample}.{l_o_s}.{step}{read}.fq.gz"),
        l_o_s = long_or_short,
        step=step,
        read=READS[long_or_short],
        sample=wildcards.sample)


rule raw_all:
    input:
        #rules.prepare_short_reads_all.input,
        #rules.prepare_long_reads_all.input,
