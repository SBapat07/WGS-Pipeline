process PROCESS_BAM {
    tag "${aligned_sam.baseName}"

    container 'staphb/samtools:latest'  // Runs only Samtools

    publishDir "${params.bwaresult}/${aligned_sam.baseName}", mode: 'copy'

    input:
     path aligned_sam

    output:
     path "${aligned_sam.baseName}_aligned.bam", emit: aligned_bam
     path "${aligned_sam.baseName}_aligned_reads.bam", emit: mapped_reads
     path "${aligned_sam.baseName}_unmapped_reads.bam", emit: unmapped_reads
     path "${aligned_sam.baseName}_stats.txt", emit: bam_stats
     path "${aligned_sam.baseName}_unmapped.fastq", emit: unmapped_fastq
     path "${aligned_sam.baseName}_aligned.fastq", emit: mapped_fastq
     

    script:
    """

    # Convert SAM to BAM
    samtools view -@ 4 -Sb -o ${aligned_sam.baseName}_aligned.bam ${aligned_sam}

    # Check BAM file integrity
    samtools quickcheck ${aligned_sam.baseName}_aligned.bam 

    # Split BAM into aligned and unmapped reads
    samtools view -b -F 4 ${aligned_sam.baseName}_aligned.bam > ${aligned_sam.baseName}_aligned_reads.bam
    samtools view -b -f 4 ${aligned_sam.baseName}_aligned.bam > ${aligned_sam.baseName}_unmapped_reads.bam

    # Compute stats
    samtools stats ${aligned_sam.baseName}_aligned.bam > ${aligned_sam.baseName}_stats.txt

    # Convert BAM to FASTQ
    samtools fastq ${aligned_sam.baseName}_aligned_reads.bam > ${aligned_sam.baseName}_aligned.fastq
    samtools fastq ${aligned_sam.baseName}_unmapped_reads.bam > ${aligned_sam.baseName}_unmapped.fastq
    """
}
