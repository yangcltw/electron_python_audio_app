// Electron Main Process
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { exec } = require('child_process');

let mainWindow;

app.on('ready', () => {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: true,
    },
  });

  mainWindow.loadFile('index.html');
});

ipcMain.handle('process-audio', async (_, audioPath) => {
  return new Promise((resolve, reject) => {
    exec(`python backend/app.py --file ${audioPath}`, (error, stdout, stderr) => {
      if (error) {
        reject(`Error: ${stderr}`);
      } else {
        resolve(stdout);
      }
    });
  });
});
