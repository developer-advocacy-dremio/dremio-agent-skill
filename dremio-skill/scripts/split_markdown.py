import os
import re
import sys

def split_markdown(input_file, output_dir, level=1):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_title = "intro"
    current_content = []
    in_code_block = False
    
    # regex for header: ^#{level} space
    # e.g. ^# for level 1, ^## for level 2
    # We want to split on this level OR higher (lower number)? 
    # Usually splitting on H1 means we keep H2s inside. 
    # If we split on H2, we keep H3s inside.
    # Let's strictly split on the target level for now, or maybe "at least this level"?
    # For sql.md (level 2), we want to split on ##.
    # For python.md (level 1), we want to split on #.
    
    header_prefix = "#" * level + " "

    def save_file(title, content):
        if not content:
            return
        slug = re.sub(r'[^a-z0-9]+', '_', title.lower()).strip('_')
        slug = slug[:50]
        if not slug:
            slug = "section"
        filename = f"{slug}.md"
        path = os.path.join(output_dir, filename)
        
        # Check collision
        counter = 1
        base_path = path
        while os.path.exists(path):
            path = base_path.replace(".md", f"_{counter}.md")
            counter += 1

        with open(path, 'w', encoding='utf-8') as out:
            out.writelines(content)
        print(f"Created: {path}")

    for line in lines:
        # Detect code block toggle
        if line.strip().startswith('```'):
            in_code_block = not in_code_block

        # Check for header NOT in code block
        # Must be at start of line (no leading spaces for top level headers usually)
        if not in_code_block and line.startswith(header_prefix):
            # Save previous
            save_file(current_title, current_content)
            
            # Start new
            current_title = line.strip()[level:].strip()
            current_content = [line]
        else:
            current_content.append(line)

    # Save last
    save_file(current_title, current_content)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python split_markdown.py <input_file> <output_dir> [level]")
        sys.exit(1)
    
    lvl = 1
    if len(sys.argv) > 3:
        lvl = int(sys.argv[3])

    split_markdown(sys.argv[1], sys.argv[2], lvl)
