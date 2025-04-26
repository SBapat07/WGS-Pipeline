process MULTIQC{

tag "${fastqc_html.baseName}"

container 'wgs-pipeline:latest'

publishDir "${params.multiqcresult}/${fastqc_html.baseName}", mode: 'copy'

input:
 path fastqc_html
 path fastqc_zip
 path trimmomatic_fastq
 path trimmomatic_log
 path fastp_fastq
 path fastp_html
 path fastp_json
 path aligned_bam
 path mapped_reads
 path unmapped_reads
 path bam_stats
 path mapped_fastq
 path unmapped_fastq
 path prokka_output
 path prokka_tsv
 
output:
 path "*", emit: multiqc_report
 
script:

"""
multiqc $fastqc_html $fastqc_zip $trimmomatic_fastq $trimmomatic_log $fastp_fastq $fastp_html $fastp_json $aligned_bam $mapped_reads $unmapped_reads $bam_stats $mapped_fastq $unmapped_fastq $prokka_output $prokka_tsv --filename ${fastqc_html.baseName}_multiqcreport.html

"""
}
