import os

ROOT_DIR = "dremio-skill/knowledge/python"

MAPPING = {
    "iceberg_management.md": [
        "iceberg_client",
        "iceberg_maintenance",
        "guide_iceberg",
        "schema_evolution",
        "slowly_changing_dimensions"
    ],
    "reflections.md": [
        "reflection_management",
        "guide_reflections",
        "ai_reflection_tools" # If it was missed or if it exists
    ],
    "security.md": [
        "security_best_practices",
        "security_patterns",
        "grants_and_privileges", # If missed
        "row_access" # If missed
    ],
    "visualization.md": [
        "charting",
        "plotting"
    ],
    "integrations.md": [
        "dlt_integration",
        "pydantic_integration",
        "notebook_integration",
        "airflow_integration", # If missed
        "s3_integration"
    ],
    "advanced_usage.md": [
        "dremioframe_cookbook",
        "deployment_guide",
        "ci_cd_deployment",
        "dremioagent_class",
        "dremio_api_compatibility",
        "troubleshooting_guide"
    ],
    "ai_integrations.md": [ 
        # Appending these to existing if possible, or just overwriting (risky if I don't handle it).
        # Actually, I'll let the script Handle 'generate_structured_data' into 'ai_integrations_extra.md' 
        # then I'll manually cat it? 
        # Or I'll just put them in 'ai_features.md' to avoid overwriting 'ai_integrations.md'
        "generate_structured_data"
    ]
}

def consolidate_cleanup():
    files = [f for f in os.listdir(ROOT_DIR) if f.endswith(".md")]
    
    for target, patterns in MAPPING.items():
        matches = []
        for f in files:
            # Skip if it's a target file already created (to avoid self-inclusion loop if running multiple times)
            if f in MAPPING.keys(): continue
            
            for p in patterns:
                if p in f:
                    matches.append(f)
                    break
        
        if not matches:
            continue
            
        matches = list(set(matches)) # Dedup
        matches.sort()
        
        target_path = os.path.join(ROOT_DIR, target)
        
        # Read existing target if it exists (for appending)
        existing_content = ""
        if os.path.exists(target_path):
            with open(target_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        
        content_buffer = []
        if existing_content:
            content_buffer.append(existing_content)
        else:
             title = target.replace('.md', '').replace('_', ' ').title()
             content_buffer.append(f"# {title}\n")
        
        for fname in matches:
            fpath = os.path.join(ROOT_DIR, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                f_content = f.read().strip()
                
                # Check headers
                lines = f_content.split('\n')
                if lines and lines[0].startswith('# '):
                    lines[0] = '#' + lines[0]
                elif lines and lines[0].startswith('## '):
                    lines[0] = '#' + lines[0]
                else:
                    title = fname.replace('.md', '').replace('_', ' ').title()
                    lines.insert(0, f"## {title}")
                
                content_buffer.append("\n".join(lines))
        
        final_content = "\n\n---\n\n".join(content_buffer)
        
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
            
        print(f"Updated {target} with {len(matches)} files.")
        
        for fname in matches:
            if fname != target:
                os.remove(os.path.join(ROOT_DIR, fname))
                print(f"Deleted {fname}")

if __name__ == "__main__":
    consolidate_cleanup()
