const { app, BrowserWindow, ipcMain, dialog } = require("electron");

function createWindow() {
  const mainWindow = new BrowserWindow({
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  let filePath;
  let bpmTolerance = 1;
  let keyTolerance = 1;

  ipcMain.on("open-file-dialog", (event) => {
    dialog
      .showOpenDialog(mainWindow, {
        properties: ["openDirectory"],
      })
      .then((result) => {
        if (!result.canceled) {
          filePath = result.filePaths[0];
          event.sender.send("file-selected", filePath);
        }
      })
      .catch((err) => {
        console.error("Error opening file dialog:", err);
      });
  });

  ipcMain.on("bpm-change", (event, newValue) => {
    bpmTolerance = newValue;
  });

  ipcMain.on("key-change", (event, newValue) => {
    keyTolerance = newValue;
  });

  ipcMain.on("run", (event) => {
    fetch(
      `http://localhost:5000/create-graph/${filePath}?bpm_tolerance=${bpmTolerance}&key_tolerance=${keyTolerance}`
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        event.sender.send("graph-received", data);
      })
      .catch((error) => {
        console.error("Error fetching graph data:", error);
      });
  });

  ipcMain.on("run-demo", (event) => {
    fetch(
      `http://localhost:5000/create-graph-demo?bpm_tolerance=${bpmTolerance}&key_tolerance=${keyTolerance}`
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        event.sender.send("graph-received", data);
      })
      .catch((error) => {
        console.error("Error fetching demo graph data:", error);
      });
  });

  mainWindow.loadFile("index.html");
}

app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});