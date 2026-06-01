/**
 * Replace deprecated jcenter() in native module Gradle files (removed in Gradle 8+).
 * Runs on postinstall so Codemagic and local npm ci stay in sync.
 */
const fs = require('fs');
const path = require('path');

const nodeModules = path.join(__dirname, '..', 'node_modules');

function walk(dir, files = []) {
  if (!fs.existsSync(dir)) {
    return files;
  }
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === '.bin' || entry.name.startsWith('.')) {
        continue;
      }
      walk(full, files);
    } else if (entry.name === 'build.gradle' || entry.name === 'build.gradle.kts') {
      files.push(full);
    }
  }
  return files;
}

let patched = 0;
for (const file of walk(nodeModules)) {
  const original = fs.readFileSync(file, 'utf8');
  if (!original.includes('jcenter()')) {
    continue;
  }
  const updated = original.replace(/jcenter\(\)/g, 'mavenCentral()');
  fs.writeFileSync(file, updated);
  patched += 1;
  console.log(`[patch-gradle-repos] jcenter() -> mavenCentral() in ${path.relative(nodeModules, file)}`);
}

if (patched === 0) {
  console.log('[patch-gradle-repos] No jcenter() references found.');
}
