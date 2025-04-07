process FASTQC {
    tag "$fastq.baseName"
    
    container 'biocontainers/fastqc:v0.11.9_cv8'
    
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
