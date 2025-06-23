process HUMANN_REGROUP {

tag "$files.baseName"

container null

publishDir "${params.metabolites}", mode: 'copy'

input:
 path files

output:
 path "*", emit: regrouped

script:

"""
humann_regroup_table --input ${files} --custom ${params.group} --output ${files.getBaseName()}_regrouped.tsv

python /home/rdadmin/Desktop/ShreyasWGS_Pipeline/WGS_Pipeline/modules/metabolites.py ${files.getBaseName()}_regrouped.tsv ${params.mapping_file}

"""
}
