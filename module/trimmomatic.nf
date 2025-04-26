process TRIMMOMATIC {
    tag "$fastq.baseName"

    container 'wgs-pipeline:latest'

    publishDir "${params.trimresult}/${fastq.baseName}", mode: 'copy'

    input:
    tuple path(fastq), path(param)

    output:
    path "${fastq.baseName}_tr.fastq", emit: trimmed_fastq
    path "${fastq.baseName}_trimmomatic.log", emit: trim_log

    script:
    """
    SEQ_TYPE=\$(awk -F '=' '/seq_type/ {print \$2}' ${param})
    SLIDINGWINDOW=\$(awk -F '=' '/SLIDINGWINDOW/ {print \$2}' ${param})
    LEADING=\$(awk -F '=' '/LEADING/ {print \$2}' ${param})
    TRAILING=\$(awk -F '=' '/TRAILING/ {print \$2}' ${param})

    trimmomatic "\$SEQ_TYPE" -phred33 ${fastq} ${fastq.baseName}_tr.fastq \\
        SLIDINGWINDOW:\$SLIDINGWINDOW \\
        LEADING:\$LEADING \\
        TRAILING:\$TRAILING \\
        2> ${fastq.baseName}_trimmomatic.log
    """
}

