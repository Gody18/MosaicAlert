import os
import re

GENERIC_BUILDSCRIPT = """
buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath "com.android.tools.build:gradle:8.12.0"
    }
}
"""

def fix_buildscript(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # If buildscript exists, update the classpath version
    if 'buildscript {' in content:
        # Regex to find any AGP classpath and replace it with 8.12.0
        new_content = re.sub(r'classpath\s+["\']com\.android\.tools\.build:gradle:[\d.]+["\']', 
                             'classpath "com.android.tools.build:gradle:8.12.0"', content)
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated buildscript in {file_path}")
            return True
    else:
        # Insert generic if missing
        new_content = GENERIC_BUILDSCRIPT + "\n" + content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Added generic buildscript to {file_path}")
        return True
    return False

def main():
    node_modules_path = 'G:/MosaicAlert/app/node_modules'
    for root, dirs, files in os.walk(node_modules_path):
        for file in files:
            if file == 'build.gradle':
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()
                    if 'com.android.library' in file_content or 'com.android.application' in file_content:
                        fix_buildscript(file_path)

if __name__ == "__main__":
    main()
