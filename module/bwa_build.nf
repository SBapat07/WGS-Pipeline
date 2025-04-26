process BWA_BUILD {

    tag "${fasta.baseName}"
    container 'staphb/bwa:latest'

    input:
    path fasta

    output:
    path "${fasta.baseName}.amb", emit: amb_file
    path "${fasta.baseName}.ann", emit: ann_file
    path "${fasta.baseName}.bwt", emit: bwt_file
    path "${fasta.baseName}.pac", emit: pac_file
    path "${fasta.baseName}.sa", emit: sa_file
     path fasta, emit: ref_file
    

    script:
    """
    bwa index -a bwtsw $fasta  
    
    """
}

