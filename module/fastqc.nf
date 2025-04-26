process FASTQC {
    tag "$fastq.baseName"
    
    container 'wgs-pipeline:latest'
    
    publishDir "${params.qcresult}/${fastq.baseName}", mode: 'copy'
    
    input:
    path fastq
    
    output:
    path "${fastq.baseName}_fastqc.zip", emit: fastqc_zip
    path "${fastq.baseName}_fastqc.html", emit: fastqc_html
    
    script:
    """
    fastqc ${fastq} -f fastq 
 
    """
}

