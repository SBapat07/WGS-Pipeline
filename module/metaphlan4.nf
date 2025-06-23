process metaphlan4 {

tag "${reads.getBaseName()}"

container null

publishDir "${params.metaphlan4result}/${reads.baseName}", mode: 'copy'

input:
 path reads

output:
 path "${reads.baseName}_abundance_profile.txt", emit: abundance_file
 path "${reads.baseName}_abundance_profile.biom", emit: biom_file
 path "${reads.baseName}_abundance.krona", emit: krona_file

script:

"""

metaphlan ${reads} \\
        --input_type fastq \\
        --bowtie2db "/home/rdadmin/Desktop/ShreyasWGS_Pipeline/WGS_Pipeline/databases/metaphlan_db" \\
        --tax_lev a \\
        --stat_q 0.1 \\
        --output_file ${reads.baseName}_abundance_profile.txt \\
        --biom ${reads.baseName}_abundance_profile.biom \\
        --nproc 16 \\

metaphlan4krona.py \\
        -p ${reads.baseName}_abundance_profile.txt \\
        -k ${reads.baseName}_abundance.krona \\
"""
}

