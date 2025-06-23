nextflow.enable.dsl=2

include { MoveInputFiles } from './modules/movefiles.nf'
include { Vsearch } from './modules/vsearch.nf'
include { FASTQC } from './modules/fastqc.nf'  
include { FASTP } from './modules/fastp.nf'
include { MULTIQC } from './modules/multiqc.nf'
include { BWA_BUILD } from './modules/bwa_build.nf'
include { ALIGNMENT } from './modules/alignment.nf'
include { PROCESS_BAM } from './modules/processing.nf'
include { metaphlan4 } from './modules/metaphlan4.nf'
include { KRONA } from './modules/krona.nf'
include {HUMAnN} from './modules/humann.nf'
include { HUMANN_REGROUP } from './modules/humann_regroup.nf'

workflow{

// 🔹 FASTQC Workflow


    log.info "\n"
    log.info "******************************************"
    log.info "🚀  Starting WGS Meatgenomics Pipeline...   "
    log.info "******************************************"
    log.info "\n"

    // ✅ Read input paired-end fastq files
    Channel
        .fromFilePairs(params.reads, flat: true)
        .set { reads_ch }

    // ✅ Vsearch merging
    merged_sample_ch = Vsearch(reads_ch)

    // ✅ Move original read1/read2 files to "Processed_Samples"
    MoveInputFiles(reads_ch)

    // ✅ FASTQC on merged FASTQ files
    fastqc_results = FASTQC(merged_sample_ch)

    // ✅ Pass fastp input
    fastp_input_ch = merged_sample_ch.map { merged_fastq -> tuple(merged_fastq, params.fastp_params) }

    // ✅ Run FASTP (assuming FASTP takes merged fastq and param file)
    fastp_results = FASTP(fastp_input_ch)

    alignment_result = ALIGNMENT(fastp_results.fptrimmed_fastp)
    
    processing_result = PROCESS_BAM(alignment_result.aligned_sam)
    
    taxonomic_result = metaphlan4(fastp_results.fptrimmed_fastp)
    
    krona_visualisation = KRONA(taxonomic_result.krona_file)
    
    humann_results = HUMAnN(processing_result.unmapped_fastq, taxonomic_result.abundance_file)
  
    multiqc_results = MULTIQC(fastqc_results, fastp_results, processing_result)

    metabolite_results = HUMANN_REGROUP(humann_results.genes)    
}


workflow.onComplete {
    log.info "\n"
    log.info "✨******************************************✨\n"
    log.info "🎉     PIPELINE EXECUTION COMPLETE!      🎉\n"
    log.info "✨******************************************✨\n"

    log.info "📊  All analyses have been successfully performed!\n"

    log.info "📂  FASTQC Reports Available at: ${params.qcresult}\n"

    log.info "⚡  Fastp Processed Reads at: ${params.fastpresult}\n"

    log.info "📃  Fastp parameter file: ${params.fastp_params}\n"

    log.info "📌  BWA output: ${params.bwaresult}\n"

    log.info "📁  MetaPhlAn output: ${params.metaphlan4result}\n"

    log.info "📊  Krona charts: ${params.kronaresult}\n"

    log.info "📦  HUMAnN output: ${params.humannresult}\n"

    // 🧹 Cleanup: delete contents inside the processing directory, not the directory itself
    def processingDir = file(params.processing)
    if (processingDir.exists() && processingDir.isDirectory()) {
        try {
            def cleanCmd = "rm -rf ${params.processing}/{*,.*}"
            ["bash", "-c", cleanCmd].execute().waitFor()
            log.info "✅ Contents inside ${params.processing} have been deleted.\n"
        } catch (Exception e) {
            log.warn "⚠️  Cleanup failed: ${e.message}\n"
        }
    } else {
        log.warn "⚠️  Directory not found or invalid: ${params.processing}\n"
    }

    def cmd = "streamlit run ${params.app_file} --server.headless true --server.enableCORS false --server.address 0.0.0.0 --server.port 8501"

    def proc = cmd.execute()

    log.info "🌐 Streamlit app started!\n"

    log.info "📺 Visit: http://192.168.1.15:8501 from your browser\n"

    log.info "🎯  Thank you for using the WGS Metagenomics Pipeline! 🎯\n"

    log.info "✨****************************************************✨"

}



