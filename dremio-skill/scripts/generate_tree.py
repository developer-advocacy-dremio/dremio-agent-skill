import os

def get_file_title(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith('# '):
                    return stripped[2:].strip()
                if stripped and not stripped.startswith('#') and not stripped.startswith('<!--'):
                    # Return first meaningful line if no H1, truncated
                    return stripped[:50] + "..."
    except Exception:
        return ""
    return ""

def generate_knowledge_tree(root_dir, output_file):
    lines = ["# Knowledge Tree\n", "This file maps all available documentation in the knowledge base.\n\n"]
    
    # Walk the directory
    for root, dirs, files in os.walk(root_dir):
        # Sort dirs and files for consistent output
        dirs.sort()
        files.sort()
        
        # Calculate depth
        rel_path = os.path.relpath(root, root_dir)
        if rel_path == ".":
            level = 0
        else:
            level = rel_path.count(os.sep) + 1
            
        indent = "  " * level
        
        # Add directory name (if not root)
        if level > 0:
            dirname = os.path.basename(root)
            lines.append(f"{indent}- **{dirname}/**\n")
            indent += "  " # Indent content of this dir
            
        # Add files
        for f in files:
            if f.endswith(".md") and f != "knowledge-tree.md":
                # Create relative link
                file_rel = os.path.join(rel_path, f)
                if rel_path == ".":
                    file_rel = f
                
                full_path = os.path.join(root, f)
                title = get_file_title(full_path)
                
                comment = ""
                if title:
                    comment = f" - *{title}*"
                
                lines.append(f"{indent}- [{f}]({file_rel}){comment}\n")

    with open(output_file, "w") as f:
        f.writelines(lines)
    print(f"Tree generated at {output_file}")

if __name__ == "__main__":
    generate_knowledge_tree("dremio-skill/knowledge", "dremio-skill/knowledge/knowledge-tree.md")
