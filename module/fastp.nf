process FASTP {
    tag "$fastq.baseName"

    container 'wgs-pipeline:latest'

    publishDir "${params.fastpresult}/${fastq.baseName}", mode: 'copy'

    input:
    tuple path(fastq), path(param_file)

    output:
    path "${fastq.baseName}_fptrimmed.fastq", emit: fptrimmed_fastp
    path "${fastq.baseName}_fpreport.html", emit: report_html
    path "${fastq.baseName}_fpreport.json", emit: report_json

    script:
    """
    CUT_WINDOW_SIZE=\$(awk -F '=' '/cut_right_window_size/ {print \$2}' ${param_file})
    CUT_MEAN_QUALITY=\$(awk -F '=' '/cut_right_mean_quality/ {print \$2}' ${param_file})

    fastp -i ${fastq} -o ${fastq.baseName}_fptrimmed.fastq \\
        --dont_overwrite -A -r \\
        --cut_right_window_size "\$CUT_WINDOW_SIZE" \\
        --cut_right_mean_quality "\$CUT_MEAN_QUALITY" -Q -L \\
        -h ${fastq.baseName}_fpreport.html \\
        -j ${fastq.baseName}_fpreport.json
    """
}

