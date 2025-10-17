// server.js
import express from 'express';
import { spawn } from 'child_process';
import cors from 'cors';

const app = express();
const PORT = 3001; // Puerto para nuestro servidor backend

app.use(cors()); // Permite que el frontend se comunique con este servidor

app.post('/run-scraper', (req, res) => {
  console.log('>>> Solicitud recibida para ejecutar el scraper...');

  // Ejecuta el comando 'python scraper/asus_scraper.py'
  const scraperProcess = spawn('python', ['scraper/asus_scraper.py']);

  // Captura la salida de la consola del script
  scraperProcess.stdout.on('data', (data) => {
    console.log(`[Scraper STDOUT]: ${data}`);
  });

  // Captura los errores del script
  scraperProcess.stderr.on('data', (data) => {
    console.error(`[Scraper STDERR]: ${data}`);
  });

  // Cuando el script termine de ejecutarse
  scraperProcess.on('close', (code) => {
    if (code === 0) {
      console.log('>>> El scraper finalizó con éxito.');
      res.status(200).json({ message: 'Scraping completado con éxito.' });
    } else {
      console.error(`>>> El scraper finalizó con un error (código: ${code}).`);
      res.status(500).json({ message: `El script finalizó con el código de error: ${code}` });
    }
  });
});

app.listen(PORT, () => {
  console.log(`🚀 Servidor backend escuchando en http://localhost:${PORT}`);
});