// scripts/merge-packages.js
const fs = require("fs-extra");
const path = require("path");

const flaskDistPath = path.resolve(__dirname, "../dist");
const electronDistPath = path.resolve(__dirname, "../dist_electron");
const packageOutputPath = path.resolve(__dirname, "../package");

// 程式輸出位置確認
fs.ensureDirSync(packageOutputPath);

// 複製 Flask 後端到 package
fs.copySync(flaskDistPath, packageOutputPath);

// 複製 Electron 前端到 package
fs.copySync(electronDistPath, packageOutputPath);

console.log("Packaging completed.");
