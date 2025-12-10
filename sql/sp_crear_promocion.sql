CREATE OR ALTER PROCEDURE sp_CrearPromocion
    @nombre VARCHAR(100),
    @descripcion VARCHAR(255),
    @valor DECIMAL(10,2),
    @fechaInicio DATETIME,
    @fechaFin DATETIME
AS
BEGIN
    SET NOCOUNT ON;
    
    INSERT INTO Promocion (nombrePromocion, descripcionPromocion, idTipoDescuento, valorDescuento, fechaInicio, fechaFin, estadoPromocion)
    VALUES (@nombre, @descripcion, 1, @valor, @fechaInicio, @fechaFin, 1);
    -- 1 = Percentage? or Amount? Defaulting TipoDescuento=1
END
