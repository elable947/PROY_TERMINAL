IF NOT EXISTS (SELECT 1 FROM Destino WHERE idProvincia = 3 AND nombreDestino = 'Chachapoyas')
BEGIN
    INSERT INTO Destino (idProvincia, nombreDestino) VALUES (3, 'Chachapoyas');
END
