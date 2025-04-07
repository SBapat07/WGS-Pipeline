process PROKKA {

tag "${fasta.baseName}"

container 'staphb/prokka'

publishDir "${params.prokkaresult}/${fasta.baseName}", mode: 'copy'

input:
 path fasta
 
output: 
 path "*", emit: prokka_output
 
script:

"""

prokka --outdir "${fasta.baseName}" --force --prefix ${fasta.baseName} --metagenome ${fasta}

"""
}
