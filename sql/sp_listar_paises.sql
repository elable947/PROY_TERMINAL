CREATE OR ALTER PROCEDURE sp_ListarPaises
AS
BEGIN
    SELECT idPais, nombrePais FROM Paises ORDER BY nombrePais;
END
