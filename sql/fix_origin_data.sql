UPDATE Ruta
SET idOrigen = 9
WHERE idOrigen = 1;

UPDATE Destino
SET nombreDestino = 'Chachapoyas'
WHERE idDestino = 9;

-- Optional: Ensure Terminal 1 corresponds to Destino 9 if there is a link
-- But for now, just fixing the Route origin FK is sufficient for the display issues.
