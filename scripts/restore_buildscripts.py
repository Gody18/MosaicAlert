import os

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

def restore_buildscript(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if 'buildscript {' not in content:
        # Insert at the beginning or after imports
        new_content = GENERIC_BUILDSCRIPT + "\n" + content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Restored generic buildscript to {file_path}")

def main():
    node_modules_path = 'G:/MosaicAlert/app/node_modules'
    for root, dirs, files in os.walk(node_modules_path):
        for file in files:
            if file == 'build.gradle':
                file_path = os.path.join(root, file)
                # Check if it was one of the files I likely modified
                # I'll check if it has 'safeExtGet' or other RN patterns
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()
                    if 'com.android.library' in file_content or 'com.android.application' in file_content:
                        restore_buildscript(file_path)

if __name__ == "__main__":
    main()
