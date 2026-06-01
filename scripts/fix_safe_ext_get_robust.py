import os

# Robust version of safeExtGet that handles both String and List of Strings
ROBUST_SAFE_EXT_GET = """
def safeExtGet(prop, fallback) {
    if (prop instanceof List) {
        for (p in prop) {
            if (rootProject.ext.has(p)) {
                return rootProject.ext.get(p)
            }
        }
        return fallback
    }
    return rootProject.ext.has(prop) ? rootProject.ext.get(prop) : fallback
}
"""

def fix_safe_ext_get(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Replace existing safeExtGet with robust version or add it if missing
    if 'def safeExtGet' in content:
        # Find the end of the existing safeExtGet function
        start_idx = content.find('def safeExtGet')
        brace_count = 0
        end_idx = -1
        for i in range(start_idx, len(content)):
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_idx = i + 1
                    break
        
        if end_idx != -1:
            new_content = content[:start_idx] + ROBUST_SAFE_EXT_GET + content[end_idx:]
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated safeExtGet to robust version in {file_path}")
    elif 'safeExtGet(' in content:
        # Add robust version at the top if it uses safeExtGet but doesn't define it
        new_content = ROBUST_SAFE_EXT_GET + "\n" + content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Added robust safeExtGet to {file_path}")

def main():
    node_modules_path = 'G:/MosaicAlert/app/node_modules'
    for root, dirs, files in os.walk(node_modules_path):
        for file in files:
            if file == 'build.gradle':
                file_path = os.path.join(root, file)
                fix_safe_ext_get(file_path)

if __name__ == "__main__":
    main()
