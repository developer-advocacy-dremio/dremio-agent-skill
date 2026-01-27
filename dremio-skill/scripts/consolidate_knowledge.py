import os

# Define the mapping of target file -> list of source files (partial matches or full names)
# We will use simple substring matching for robustness against slug variations
MAPPING = {
    "data_quality.md": [
        "check_that_",
        "custom_check_row_count",
        "data_quality_",
        "sql_linting",
        "will_raise_validationerror",
        "check_cost_before_running_expensive_query"
    ],
    "orchestration_and_pipelines.md": [
        "orchestration_",
        "airflow_integration",
        "dremio_job_integration",
        "incremental_processing",
        "3_run_pipeline",
        "add_tasks",
        "2_start_ui_server",
        "note_in_production",
        "batch_operations",
        "distributed_execution"
    ],
    "transformations.md": [
        "case_when",
        "coalesce",
        "convert_",
        "flatten_an_array",
        "fetches_all_data",
        "filters_in_dremio",
        "in_mutate",
        "in_select",
        "joins",
        "aggregation",
        "array_"
    ],
    "ai_integrations.md": [
        "ai_",
        "dremio_ai_",
        "dremio_agent_",
        "using_mcp_tools"
    ],
    "ingestion_and_loading.md": [
        "ingestion_",
        "load_",
        "create_from_data",
        "create_large_dataset",
        "insert_in_batches",
        "upsert_from_a_dataframe",
        "use_staging_method",
        "file_system_ingestion",
        "file_upload",
        "database_ingestion",
        "document_extraction"
    ],
    "testing.md": [
        "run_all_unit_tests",
        "create_mock_client",
        "tests_conftest",
        "retrieve_loaded_fixture",
        "exact_match",
        "partial_match",
        "this_will_match",
        "configure_a_response",
        "use_in_your_code"
    ],
    "setup_and_configuration.md": [
        "connecting_to_dremio",
        "configuration_reference",
        "create_a_pool",
        "optional_dependencies",
        "python_sdk_setup_quickstart", # Keep quickstart separate? Maybe merge config into it.
        # Actually I'll merge config INTO quickstart or make a setup file. 
        # Let's keep python_sdk_setup_quickstart.md as the target and merge others into it?
        # No, standardized naming is better.
    ],
    "performance_tuning.md": [
        "cache_the_result",
        "local_caching",
        "default_batch_size",
        "subsequent_operations",
        "query_profile_analyzer",
        "output_query_2",
        "iteratively_improve_query",
        "review_all_queries"
    ],
    "catalog_admin.md": [
        "catalog_admin", # Source file
        "list_root_catalog",
        "list_specific_path",
        "grants_and_privileges",
        "row_access_and_column_masking",
        "dataset_tagging",
        "documenting_datasets",
        "space_and_folder_management",
        "udf_manager"
    ]
}

ROOT_DIR = "dremio-skill/knowledge/python"

def consolidate():
    files = [f for f in os.listdir(ROOT_DIR) if f.endswith(".md")]
    merged_files = set()
    
    for target, patterns in MAPPING.items():
        # Find matches
        matches = []
        for f in files:
            if f in merged_files: continue
            for p in patterns:
                if p in f:
                    matches.append(f)
                    break
        
        if not matches:
            continue

        # Sort matches to keep some order (maybe alphabetic is ok, or try to be smarter)
        matches.sort()
        
        # Determine content
        target_path = os.path.join(ROOT_DIR, target)
        
        # If target already exists and is NOT in matches (e.g. we are appending to an existing main file)
        # We should read it first.
        # But for this script, I assume we are creating NEW thematic files or overwriting.
        # Ideally we read, and if it's a "main" file (like catalog_admin.md), we put it first.
        
        content_buffer = []
        
        # Prioritize exact match to target name or "main" looking files
        priority_files = [m for m in matches if m == target or "overview" in m or "framework" in m]
        other_files = [m for m in matches if m not in priority_files]
        
        sorted_matches = priority_files + other_files
        
        for fname in sorted_matches:
            fpath = os.path.join(ROOT_DIR, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                f_content = f.read().strip()
                # Remove top level header if it duplicates or downgrade it?
                # We will downgrade headers by 1 level if we are merging?
                # No, the previous split made them H1. We should probably make them H2 in the merged file
                # EXCEPT for the very first one if it's the title.
                
                # Actually, let's just append with a separator.
                # And ensure the header is H1 or H2 appropriately.
                # If we are merging into "Data Quality", we want the file to have a H1 "Data Quality".
                # And the sub-files to be H2.
                
                # Check if file starts with #
                lines = f_content.split('\n')
                if lines and lines[0].startswith('# '):
                    lines[0] = '#' + lines[0] # Demote to H2
                elif lines and lines[0].startswith('## '):
                    lines[0] = '#' + lines[0] # Demote to H3
                else:
                    # No header? Add one based on filename
                    title = fname.replace('.md', '').replace('_', ' ').title()
                    lines.insert(0, f"## {title}")
                
                content_buffer.append("\n".join(lines))
            
            merged_files.add(fname)
            
        # Write target
        # Add a H1 title
        title = target.replace('.md', '').replace('_', ' ').title()
        final_content = f"# {title}\n\n" + "\n\n---\n\n".join(content_buffer)
        
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
            
        print(f"Created {target} from {len(sorted_matches)} files.")
        
        # Delete sources (unless source is target)
        for fname in sorted_matches:
            if fname != target:
                os.remove(os.path.join(ROOT_DIR, fname))
                print(f"Deleted {fname}")

if __name__ == "__main__":
    consolidate()
