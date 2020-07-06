rule trimming_long_reads_porechop:
    input:
        lambda wildcards: get_reads(wildcards, "long", "raw")
    output:
        os.path.join(
            config["output"]["trimming"],
            "long_reads/{sample}/{sample}.long.trimming.fq.gz")
    log:
        os.path.join(config["output"]["trimming"],
                     "logs/{sample}.long.trimming.log")
    threads:
        config["params"]["trimming"]["porechop"]["threads"]
    shell:
        '''
        porechop \
        --input {input} \
        --output {output} \
        --format fastq.gz \
        --threads {threads} \
        > {log}
        '''

       
rule trimming_long_reads_porechop_all:
    input:
        expand(os.path.join(
            config["output"]["trimming"],
            "long_reads/{sample}/{sample}.long.trimming.fq.gz"),
               sample=SAMPLES.index.unique())


rule trimming_all:
    input:
        rules.trimming_long_reads_porechop_all.input
