process KRONA{

tag "${file.baseName}"

container 'wgs-pipeline:latest'

publishDir "${params.metaphlanresult}/${file.baseName}", mode: 'copy'

input:
 path file
 
output:
 path "${file.baseName}_Krona_Plot.html", emit: krona_plot
 
script:

"""

ktImportText ${file} -o ${file.baseName}_Krona_Plot.html

"""
}
