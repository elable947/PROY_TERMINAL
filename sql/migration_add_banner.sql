IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[EmpresaTransporte]') AND name = 'bannerUrl')
BEGIN
    ALTER TABLE EmpresaTransporte ADD bannerUrl VARCHAR(500) NULL;
END
GO
UPDATE EmpresaTransporte SET bannerUrl = 'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&q=80' WHERE bannerUrl IS NULL;
