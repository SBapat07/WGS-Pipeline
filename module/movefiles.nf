process MoveInputFiles {
    tag "${sample_id}"

    container null

    stageInMode 'copy'

    input:
    tuple val(sample_id), path(read1), path(read2)

    script:
    """
    mkdir -p ${params.processed}
    mv ${read1} ${params.processed}/
    mv ${read2} ${params.processed}/
    
    """
}
