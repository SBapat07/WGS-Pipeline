process ALIGNMENT {
    tag "${reads.baseName}"
    
    container null

    publishDir "${params.bwaresult}/${reads.baseName}", mode: 'copy'

    input:
     path reads
     

    output:
     path "${reads.baseName}_aligned.sam", emit: aligned_sam

    script:
    """
    # Alignment using BWA
    bwa mem -t 16 /home/rdadmin/Desktop/ShreyasWGS_Pipeline/WGS_Pipeline/GRCh37.fa ${reads} > ${reads.baseName}_aligned.sam
    """
}
