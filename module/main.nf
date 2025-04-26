nextflow.enable.dsl=2

include { FASTQC } from './modules/fastqc.nf' 
include { TRIMMOMATIC } from './modules/trimmomatic.nf' 
include { FASTP } from './modules/fastp.nf'
include { MULTIQC } from './modules/multiqc.nf'
include { BWA_BUILD } from './modules/bwa_build.nf'
include { ALIGNMENT } from './modules/alignment.nf'
include { PROCESS_BAM } from './modules/processing.nf'
include { METAPHLAN } from './modules/metaphlan.nf'
include { KRONA } from './modules/krona.nf'
include { MEGAHIT } from './modules/megahit.nf'
include { PROKKA } from './modules/prokka.nf'


workflow{

// ✅ Declare input channel
// Load all fastq files
fastq_ch = Channel.fromPath(params.fastq, checkIfExists: true)

// Load trimming param file once
param_ch = Channel.value(file(params.trimmomatic_params))

// Combine each FASTQ with the same param file
trimmomatic_input = fastq_ch.map { fastq -> tuple(fastq, file(params.trimmomatic_params)) }

fastp_input_ch = fastq_ch.map { fastq -> tuple(fastq, file(params.fastp_params)) }





// 🔹 FASTQC Workflow


    log.info "\n"
    log.info "******************************************"
    log.info "🚀  Starting WGS Meatgenomics Pipeline...   "
    log.info "******************************************"
    log.info "\n"

    
    fastqc_results = FASTQC(fastq_ch)
    
    trimmomatic_results = TRIMMOMATIC(trimmomatic_input)
    
    fastp_results = FASTP(fastp_input_ch)

    alignment_result = ALIGNMENT(fastp_results.fptrimmed_fastp)
    
    processing_result = PROCESS_BAM(alignment_result.aligned_sam)
    
    taxonomic_result = METAPHLAN(fastp_results.fptrimmed_fastp)
    
    krona_visualisation = KRONA(taxonomic_result.krona_file)
    
    megahit_result = MEGAHIT(fastp_results.fptrimmed_fastp)
    
    prokka_result = PROKKA(megahit_result.contigs)
    
    multiqc_results = MULTIQC(fastqc_results, trimmomatic_results, fastp_results, processing_result, prokka_result)
    
    
}


workflow.onComplete{

    log.info "\n"
    log.info "✨******************************************✨\n"
    log.info "🎉     PIPELINE EXECUTION COMPLETE!      🎉\n"
    log.info "✨******************************************✨\n"

    log.info "📊  All analyses have been successfully performed!\n"

    log.info "📂  FASTQC Reports Available at: ${params.qcresult}\n"
    log.info "✂️  Trimmomatic Trimmed Reads at: ${params.trimresult}\n"
    log.info "⚡  Fastp Processed Reads at: ${params.fastpresult}\n"
    log.info "🛠️  If you want to review the parameters used for trimming, check the files below:\n"
    log.info "     📝  Trimmomatic parameter file: ${params.trimmomatic_params}\n"
    log.info "     📃  Fastp parameter file: ${params.fastp_params}\n"
    
    log.info "🔍  Host contamination filtering is complete!\n"
    log.info "🧬  Reference Genome Used: Human GRCh37\n"
    log.info "📌  You can find the results at: ${params.bwaresult}\n"
    
    
    log.info "🧫  Taxonomic classification is complete! 🧬\n"
    log.info "📁  MetaPhlAn output available at: ${params.metaphlanresult}\n"
    log.info "📊  Interactive Krona charts available at: ${params.metaphlanresult}\n"
    
    log.info "🧱  Assembly with MEGAHIT is successfully completed!\n"
log.info "📦  Assembled contigs are saved in: ${params.megahitresult}\n"


    log.info "🧪  Functional Annotation Completed with Prokka!\n"
    log.info "📁  Prokka output directory: ${params.prokkaresult}\n"
    
    def cmd = "streamlit run ${params.app_file}"
    def_proc = cmd.execute()
    log.info "🌐 Streamlit app started!\n"
    log.info "📺 Visit: http://localhost:8501\n"

    log.info "🎯  Thank you for using the WGS Metagenomics Pipeline! 🎯\n"
    log.info "✨******************************************✨\n"
    
}

