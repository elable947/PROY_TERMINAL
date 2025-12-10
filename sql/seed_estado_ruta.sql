IF NOT EXISTS (SELECT 1 FROM EstadoViaje WHERE idEstadoViaje = 4)
BEGIN
    SET IDENTITY_INSERT EstadoViaje ON;
    INSERT INTO EstadoViaje (idEstadoViaje, nombreEstadoViaje) VALUES (4, 'En Ruta');
    SET IDENTITY_INSERT EstadoViaje OFF;
END
