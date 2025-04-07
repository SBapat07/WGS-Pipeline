process FASTP {
    tag "$fastq.baseName"

    container 'staphb/fastp'

    publishDir "${params.fastpresult}/${fastq.baseName}", mode: 'copy'

    input:
    path fastq
    path file

    output:
    path "${fastq.baseName}_fptrimmed.fastq", emit: fptrimmed_fastp
    path "${fastq.baseName}_fpreport.html", emit: report_html
    path "${fastq.baseName}_fpreport.json", emit: report_json

    script:
    """
    
    CUT_WINDOW_SIZE=\$(awk -F '=' '/cut_right_window_size/ {print \$2}' fastp_params.txt)
    CUT_MEAN_QUALITY=\$(awk -F '=' '/cut_right_mean_quality/ {print \$2}' fastp_params.txt)
    
    fastp -i ${fastq} -o ${fastq.baseName}_fptrimmed.fastq --dont_overwrite -A -r --cut_right_window_size "\$CUT_WINDOW_SIZE" --cut_right_mean_quality "\$CUT_MEAN_QUALITY" -Q -L -h ${fastq.baseName}_fpreport.html -j ${fastq.baseName}_fpreport.json
                             
    """
}

