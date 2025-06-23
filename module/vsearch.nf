process Vsearch {

    tag "${sample_id}"

    container 'wgs-pipeline:latest'

    publishDir "${params.mergedfiles}", mode: 'copy'

    input:
    tuple val(sample_id), path(read1), path(read2)

    output:
    path("${sample_id}.fastq")

    script:
    """
    vsearch \\
        --fastq_mergepairs ${read1} \\
        --reverse ${read2} \\
        --fastqout ${sample_id}.fastq \\
        --fastq_minovlen 10 \\
        --fastq_maxdiffs 5
 
    """
}


