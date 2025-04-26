process PROKKA {

tag "${fasta.baseName}"

container 'wgs-pipeline:latest'

publishDir "${params.prokkaresult}", mode: 'copy'

input:
 path fasta
 
output: 
 path "*", emit: prokka_output
 path "${fasta.baseName}/*.tsv", emit: prokka_output_tsv
 
script:

"""

prokka --force --prefix ${fasta.baseName} --metagenome ${fasta}

"""
}
