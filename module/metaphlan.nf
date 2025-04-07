process METAPHLAN {

tag "${reads.baseName}"

container 'biobakery/metaphlan2:2.7.7_cloud_r1'

publishDir "${params.metaphlanresult}/${reads.baseName}", mode: 'copy'

input: 
 path reads
 
output:
 path "${reads.baseName}_abundance_profile.txt", emit: abundance_file
 path "${reads.baseName}_abundance_profile.biom", emit: biom_file
 path "${reads.baseName}_abundance.krona", emit: krona_file
 
script:

"""

python /usr/local/bin/metaphlan2.py '${reads}' --input_type fastq --tax_lev 'a' --stat_q 0.1 -t rel_ab_w_read_stats -o ${reads.baseName}_abundance_profile.txt --biom ${reads.baseName}_abundance_profile.biom

python /usr/local/bin/metaphlan2krona.py -p ${reads.baseName}_abundance_profile.txt -k ${reads.baseName}_abundance.krona 

"""
}
