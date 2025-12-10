CREATE OR ALTER PROCEDURE sp_ListarDestinos
AS
BEGIN
    SET NOCOUNT ON;
    SELECT idDestino, nombreDestino 
    FROM Destino 
    ORDER BY nombreDestino;
END
