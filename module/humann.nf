process HUMAnN {

tag "${reads.baseName}"

container null

publishDir "${params.humannresult}", mode: 'copy'

input:
 path reads
 path taxo_profile

output:
  path "${reads.getBaseName()}_humann_output/*_genefamilies.tsv", emit: genes
  path "${reads.getBaseName()}_humann_output/*", emit: humann_results


script:

"""
mkdir -p ${reads.getBaseName()}_humann_output

humann \
  --input ${reads} \
  --output ${reads.getBaseName()}_humann_output \
  --nucleotide-database ${params.nucleotide_db} \
  --protein-database ${params.protein_db} \
  --metaphlan-option "--bowtie2db /home/rdadmin/Desktop/ShreyasWGS_Pipeline/WGS_Pipeline/databases/metaphlan_db" \
  --thread 16 \
  --taxonomic-profile ${taxo_profile} \
  --o-log ${reads.getBaseName()}.log \
  --pathways metacyc \
  --output-format tsv \
  --input-format fastq \
  --search-mode uniref90

"""
}

