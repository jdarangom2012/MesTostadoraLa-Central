-- =============================================================
-- sql_setup.sql
-- Tablas y Stored Procedures para curvas de tueste/enfriamiento
-- PLC Modicon M221 TM221CE40R
-- =============================================================

USE TU_BASE_DATOS;   -- ← Cambia por tu base de datos
GO

-- =============================================================
-- 1. TABLA CURVAS TUESTE  (datos de Hoja1 — bloque %MW500-537)
-- =============================================================
IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'tblCurvasTueste')
BEGIN
    CREATE TABLE dbo.tblCurvasTueste (
        Id                  BIGINT IDENTITY(1,1) PRIMARY KEY,
        FechaRegistro       DATETIME2(0)    NOT NULL DEFAULT SYSDATETIME(),

        -- Identificación de la orden
        Orden               BIGINT          NULL,  -- %MD500 UDINT 32bit
        ClienteId           INT             NULL,  -- %MW502 UINT
        ClienteNombre       VARCHAR(20)     NULL,  -- %MW503-512 STRING
        PerfilTueste        INT             NULL,  -- %MW513 UINT

        -- Pesos
        PesoCafVerde        FLOAT           NULL,  -- %MF514 REAL (kg)
        PesoCafTostado      FLOAT           NULL,  -- %MF522 REAL (kg)

        -- Fechas y horas (almacenadas como texto legible desde BCD)
        FechaIniOrden       VARCHAR(10)     NULL,  -- %MD516 BCD → 'DD/MM/YYYY'
        HoraIniOrden        VARCHAR(8)      NULL,  -- %MD518 BCD → 'HH:MM:SS'
        FechaFinOrden       VARCHAR(10)     NULL,  -- %MD532 BCD → 'DD/MM/YYYY'
        HoraFinOrden        VARCHAR(8)      NULL,  -- %MD534 BCD → 'HH:MM:SS'

        -- Consumos
        ConsumoGas          INT             NULL,  -- %MW520 UINT (nm3)
        ConsumoKwh          INT             NULL,  -- %MW521 UINT (kWh)

        -- Temperaturas (°C enteras desde el PLC)
        TempDesh            INT             NULL,  -- %MW524
        TempRecu            INT             NULL,  -- %MW526
        Temp1Crack          INT             NULL,  -- %MW528
        TempFinCurva        INT             NULL,  -- %MW530

        -- Tiempos en segundos (convertidos desde BCD en Python)
        TiempoDesh          TIME(0)         NULL,  -- %MW525 → convertido
        TiempoRecu          TIME(0)         NULL,  -- %MW527
        Tiempo1Crack        TIME(0)         NULL,  -- %MW529
        TiempoFinCurva      TIME(0)         NULL,  -- %MW531
        TiempoTueste        TIME(0)         NULL,  -- %MW536
        TiempoEnfriamiento  TIME(0)         NULL,  -- %MW537
    );

    CREATE INDEX IX_CurvasTueste_Orden
        ON dbo.tblCurvasTueste (Orden);
    CREATE INDEX IX_CurvasTueste_Fecha
        ON dbo.tblCurvasTueste (FechaRegistro DESC);

    PRINT 'Tabla dbo.tblCurvasTueste creada.';
END
ELSE
    PRINT 'Tabla dbo.tblCurvasTueste ya existe.';
GO

-- =============================================================
-- 2. TABLA CURVAS ENFRIAMIENTO  (Hoja2 — bloque %MW600-637)
-- =============================================================
IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'tblCurvasEnfriamiento')
BEGIN
    CREATE TABLE dbo.tblCurvasEnfriamiento (
        Id                  BIGINT IDENTITY(1,1) PRIMARY KEY,
        FechaRegistro       DATETIME2(0)    NOT NULL DEFAULT SYSDATETIME(),

        Orden               BIGINT          NULL,
        ClienteId           INT             NULL,
        ClienteNombre       VARCHAR(20)     NULL,
        PerfilTueste        INT             NULL,
        PesoCafVerde        FLOAT           NULL,
        PesoCafTostado      FLOAT           NULL,
        FechaIniOrden       VARCHAR(10)     NULL,
        HoraIniOrden        VARCHAR(8)      NULL,
        FechaFinOrden       VARCHAR(10)     NULL,
        HoraFinOrden        VARCHAR(8)      NULL,
        ConsumoGas          INT             NULL,
        ConsumoKwh          INT             NULL,
        TempDesh            INT             NULL,
        TempRecu            INT             NULL,
        Temp1Crack          INT             NULL,
        TempFinCurva        INT             NULL,
        TiempoDesh          TIME(0)         NULL,
        TiempoRecu          TIME(0)         NULL,
        Tiempo1Crack        TIME(0)         NULL,
        TiempoFinCurva      TIME(0)         NULL,
        TiempoTueste        TIME(0)         NULL,
        TiempoEnfriamiento  TIME(0)         NULL,
    );

    CREATE INDEX IX_CurvasEnfr_Orden
        ON dbo.tblCurvasEnfriamiento (Orden);
    CREATE INDEX IX_CurvasEnfr_Fecha
        ON dbo.tblCurvasEnfriamiento (FechaRegistro DESC);

    PRINT 'Tabla dbo.tblCurvasEnfriamiento creada.';
END
ELSE
    PRINT 'Tabla dbo.tblCurvasEnfriamiento ya existe.';
GO

-- =============================================================
-- 3. SP TUESTE
-- =============================================================
CREATE OR ALTER PROCEDURE dbo.sp_InsertarCurvaTueste
(
    @Orden               BIGINT          = NULL,
    @ClienteId           INT             = NULL,
    @ClienteNombre       VARCHAR(20)     = NULL,
    @PerfilTueste        INT             = NULL,
    @PesoCafVerde        FLOAT           = NULL,
    @FechaIniOrden       VARCHAR(10)     = NULL,
    @HoraIniOrden        VARCHAR(8)      = NULL,
    @ConsumoGas          INT             = NULL,
    @ConsumoKwh          INT             = NULL,
    @PesoCafTostado      FLOAT           = NULL,
    @TempDesh            INT             = NULL,
    @TiempoDesh_seg      INT             = NULL,
    @TempRecu            INT             = NULL,
    @TiempoRecu_seg      INT             = NULL,
    @Temp1Crack          INT             = NULL,
    @Tiempo1Crack_seg    INT             = NULL,
    @TempFinCurva        INT             = NULL,
    @TiempoFinCurva_seg  INT             = NULL,
    @FechaFinOrden       VARCHAR(10)     = NULL,
    @HoraFinOrden        VARCHAR(8)      = NULL,
    @TiempoTueste_seg    INT             = NULL,
    @TiempoEnfr_seg      INT             = NULL
)
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    -- Función auxiliar: segundos → TIME(0)
    -- DATEADD(SECOND, N, '00:00:00') maneja hasta 23:59:59 (86399 seg)
    DECLARE
        @tDesh   TIME(0) = CAST(DATEADD(SECOND, ISNULL(@TiempoDesh_seg,0),   '00:00:00') AS TIME(0)),
        @tRecu   TIME(0) = CAST(DATEADD(SECOND, ISNULL(@TiempoRecu_seg,0),   '00:00:00') AS TIME(0)),
        @t1Crk   TIME(0) = CAST(DATEADD(SECOND, ISNULL(@Tiempo1Crack_seg,0), '00:00:00') AS TIME(0)),
        @tFin    TIME(0) = CAST(DATEADD(SECOND, ISNULL(@TiempoFinCurva_seg,0),'00:00:00') AS TIME(0)),
        @tTueste TIME(0) = CAST(DATEADD(SECOND, ISNULL(@TiempoTueste_seg,0), '00:00:00') AS TIME(0)),
        @tEnfr   TIME(0) = CAST(DATEADD(SECOND, ISNULL(@TiempoEnfr_seg,0),   '00:00:00') AS TIME(0));

    BEGIN TRY
        INSERT INTO dbo.tblCurvasTueste (
            Orden, ClienteId, ClienteNombre, PerfilTueste,
            PesoCafVerde, PesoCafTostado,
            FechaIniOrden, HoraIniOrden, FechaFinOrden, HoraFinOrden,
            ConsumoGas, ConsumoKwh,
            TempDesh, TempRecu, Temp1Crack, TempFinCurva,
            TiempoDesh, TiempoRecu, Tiempo1Crack, TiempoFinCurva,
            TiempoTueste, TiempoEnfriamiento
        )
        VALUES (
            @Orden, @ClienteId, @ClienteNombre, @PerfilTueste,
            @PesoCafVerde, @PesoCafTostado,
            @FechaIniOrden, @HoraIniOrden, @FechaFinOrden, @HoraFinOrden,
            @ConsumoGas, @ConsumoKwh,
            @TempDesh, @TempRecu, @Temp1Crack, @TempFinCurva,
            @tDesh, @tRecu, @t1Crk, @tFin,
            @tTueste, @tEnfr
        );

        SELECT SCOPE_IDENTITY() AS IdInsertado;
    END TRY
    BEGIN CATCH
        THROW;
    END CATCH
END;
GO
PRINT 'SP dbo.sp_InsertarCurvaTueste OK';
GO

-- =============================================================
-- 4. SP ENFRIAMIENTO  (misma firma, distinta tabla)
-- =============================================================
CREATE OR ALTER PROCEDURE dbo.sp_InsertarCurvaEnfriamiento
(
    @Orden               BIGINT          = NULL,
    @ClienteId           INT             = NULL,
    @ClienteNombre       VARCHAR(20)     = NULL,
    @PerfilTueste        INT             = NULL,
    @PesoCafVerde        FLOAT           = NULL,
    @FechaIniOrden       VARCHAR(10)     = NULL,
    @HoraIniOrden        VARCHAR(8)      = NULL,
    @ConsumoGas          INT             = NULL,
    @ConsumoKwh          INT             = NULL,
    @PesoCafTostado      FLOAT           = NULL,
    @TempDesh            INT             = NULL,
    @TiempoDesh_seg      INT             = NULL,
    @TempRecu            INT             = NULL,
    @TiempoRecu_seg      INT             = NULL,
    @Temp1Crack          INT             = NULL,
    @Tiempo1Crack_seg    INT             = NULL,
    @TempFinCurva        INT             = NULL,
    @TiempoFinCurva_seg  INT             = NULL,
    @FechaFinOrden       VARCHAR(10)     = NULL,
    @HoraFinOrden        VARCHAR(8)      = NULL,
    @TiempoTueste_seg    INT             = NULL,
    @TiempoEnfr_seg      INT             = NULL
)
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE
        @tDesh   TIME(0) = CAST(DATEADD(SECOND, ISNULL(@TiempoDesh_seg,0),   '00:00:00') AS TIME(0)),
        @tRecu   TIME(0) = CAST(DATEADD(SECOND, ISNULL(@TiempoRecu_seg,0),   '00:00:00') AS TIME(0)),
        @t1Crk   TIME(0) = CAST(DATEADD(SECOND, ISNULL(@Tiempo1Crack_seg,0), '00:00:00') AS TIME(0)),
        @tFin    TIME(0) = CAST(DATEADD(SECOND, ISNULL(@TiempoFinCurva_seg,0),'00:00:00') AS TIME(0)),
        @tTueste TIME(0) = CAST(DATEADD(SECOND, ISNULL(@TiempoTueste_seg,0), '00:00:00') AS TIME(0)),
        @tEnfr   TIME(0) = CAST(DATEADD(SECOND, ISNULL(@TiempoEnfr_seg,0),   '00:00:00') AS TIME(0));

    BEGIN TRY
        INSERT INTO dbo.tblCurvasEnfriamiento (
            Orden, ClienteId, ClienteNombre, PerfilTueste,
            PesoCafVerde, PesoCafTostado,
            FechaIniOrden, HoraIniOrden, FechaFinOrden, HoraFinOrden,
            ConsumoGas, ConsumoKwh,
            TempDesh, TempRecu, Temp1Crack, TempFinCurva,
            TiempoDesh, TiempoRecu, Tiempo1Crack, TiempoFinCurva,
            TiempoTueste, TiempoEnfriamiento
        )
        VALUES (
            @Orden, @ClienteId, @ClienteNombre, @PerfilTueste,
            @PesoCafVerde, @PesoCafTostado,
            @FechaIniOrden, @HoraIniOrden, @FechaFinOrden, @HoraFinOrden,
            @ConsumoGas, @ConsumoKwh,
            @TempDesh, @TempRecu, @Temp1Crack, @TempFinCurva,
            @tDesh, @tRecu, @t1Crk, @tFin,
            @tTueste, @tEnfr
        );

        SELECT SCOPE_IDENTITY() AS IdInsertado;
    END TRY
    BEGIN CATCH
        THROW;
    END CATCH
END;
GO
PRINT 'SP dbo.sp_InsertarCurvaEnfriamiento OK';
GO

-- =============================================================
-- 5. CONSULTAS ÚTILES
-- =============================================================

-- Últimas 20 curvas de tueste
-- SELECT TOP 20 * FROM dbo.tblCurvasTueste ORDER BY FechaRegistro DESC;

-- Rendimiento por cliente (kg tostado / kg verde)
-- SELECT
--     ClienteNombre,
--     COUNT(*) AS Tuestes,
--     AVG(PesoCafVerde)            AS PesoVerde_Prom,
--     AVG(PesoCafTostado)          AS PesoTostado_Prom,
--     AVG(PesoCafTostado * 100.0
--         / NULLIF(PesoCafVerde,0)) AS Rendimiento_Pct,
--     AVG(ConsumoGas)              AS Gas_Prom,
--     AVG(ConsumoKwh)              AS Kwh_Prom
-- FROM dbo.tblCurvasTueste
-- GROUP BY ClienteNombre
-- ORDER BY ClienteNombre;
