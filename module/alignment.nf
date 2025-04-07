process ALIGNMENT {
    tag "${reads.baseName}"
    
    container = null

    publishDir "${params.bwaresult}/${reads.baseName}", mode: 'copy'

    input:
     path reads
     

    output:
     path "${reads.baseName}_aligned.sam", emit: aligned_sam

    script:
    """
    # Alignment using BWA
    bwa mem /home/ghadmin/Desktop/WGS_Pipeline/modules/GRCh37.fa ${reads} > ${reads.baseName}_aligned.sam
    """
}

