import os

SAFE_EXT_GET = """
def safeExtGet(prop, fallback) {
    rootProject.ext.has(prop) ? rootProject.ext.get(prop) : fallback
}
"""

def fix_missing_safe_ext_get(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if 'safeExtGet(' in content and 'def safeExtGet' not in content:
        new_content = SAFE_EXT_GET + "\n" + content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed missing safeExtGet in {file_path}")

def main():
    node_modules_path = 'G:/MosaicAlert/app/node_modules'
    for root, dirs, files in os.walk(node_modules_path):
        for file in files:
            if file == 'build.gradle':
                file_path = os.path.join(root, file)
                fix_missing_safe_ext_get(file_path)

if __name__ == "__main__":
    main()
