process MEGAHIT {

tag "${reads.baseName}"

container 'nanozoo/megahit:latest'

publishDir params.megahitresult, mode: 'copy'

input:
 path reads
 
output:
 path "${reads.baseName}", emit: megahit_result
 path "${reads.baseName}/${reads.baseName}_final.contigs.fa", emit: contigs
 
script:

"""
megahit -r ${reads} --presets meta-sensitive -o ${reads.baseName}

# Rename final.contigs.fa to <sample>_final.contigs.fa
    mv ${reads.baseName}/final.contigs.fa ${reads.baseName}/${reads.baseName}_final.contigs.fa

"""
}
