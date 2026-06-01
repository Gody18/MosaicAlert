import os
import re

def remove_buildscript(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove buildscript { ... } block
    # This regex is a bit simplistic but should work for most cases
    # It finds buildscript { followed by everything until the matching closing brace
    # Actually, matching nested braces is easier with a simple counter
    
    if 'buildscript {' in content:
        start_idx = content.find('buildscript {')
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
            new_content = content[:start_idx] + content[end_idx:]
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Removed buildscript from {file_path}")
            return True
    return False

def main():
    node_modules_path = 'G:/MosaicAlert/app/node_modules'
    for root, dirs, files in os.walk(node_modules_path):
        for file in files:
            if file == 'build.gradle':
                file_path = os.path.join(root, file)
                # Check if it contains AGP dependency
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    if 'com.android.tools.build:gradle' in f.read():
                        remove_buildscript(file_path)

if __name__ == "__main__":
    main()
