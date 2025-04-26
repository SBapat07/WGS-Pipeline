process REPORT {

    publishDir "${params.reportresult}", mode: 'copy'
    
    container 'wgs-pipeline:latest'

    input:
    path metaphlan_out           // abundance_file (MetaPhlAn)
    path prokka_out              // prokka_file
    path krona_html_file         // krona.html

    output:
    
    path "final_report.html"

    

    script:
    """
    python3 /pipeline/report.py ${prokka_out} ${metaphlan_out} ${krona_html_file} > final_report.html
    """
}

