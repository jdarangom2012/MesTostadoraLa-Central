USE [dbTostadoraCentral]
GO
/****** Object:  Table [dbo].[tblCafeEmpaque]    Script Date: 1/09/2025 8:21:19 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblCafeEmpaque](
	[Id] [int] NOT NULL,
	[EmpaqueCafe] [varchar](50) NULL,
 CONSTRAINT [PK_tblCafeEmpaque] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblClientes]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblClientes](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[IdtipoCliente] [int] NULL,
	[IdTipoIdentificacion] [int] NULL,
	[IdEstadoCliente] [int] NULL,
	[FechaIngreso] [datetime] NULL,
	[Codigo] [varchar](25) NULL,
	[Nombre] [varchar](50) NULL,
	[Apellidos] [varchar](50) NULL,
	[Telefono] [varchar](30) NULL,
	[Direccion] [varchar](35) NULL,
	[Email] [varchar](30) NULL,
	[created_at] [datetime2](0) NOT NULL,
	[updated_at] [datetime2](0) NULL,
 CONSTRAINT [PK_tblClientes] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblCurvasTueste]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblCurvasTueste](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[FechaIngreso] [datetime] NULL,
	[TempSetPont] [int] NULL,
	[TempTost] [int] NULL,
	[PorcentajeAire] [int] NULL,
	[PorcentajeGas] [int] NULL,
 CONSTRAINT [PK_tblCurvasTueste] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblEmpaques]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblEmpaques](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[FechaIngreso] [datetime] NULL,
	[IdOrden] [int] NULL,
	[IdOrdenEmpaque] [int] NULL,
	[IdInvenCafe] [int] NULL,
	[IdEstadoTareas] [int] NULL,
	[IdTamano] [int] NULL,
	[CantEmpaque] [int] NULL,
	[CantEmpacada] [int] NULL,
	[CantEtiquetas] [int] NULL,
	[EmpClientes] [int] NULL,
	[TotalEmpaques] [int] NULL,
	[TotalEtiquetas] [int] NULL,
	[TotalPaquetes] [int] NULL,
	[Notas] [varchar](40) NULL,
	[created_at] [datetime2](0) NOT NULL,
	[updated_at] [datetime2](0) NULL,
 CONSTRAINT [PK_tblEmpaques] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblEstadoCafe]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblEstadoCafe](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[EstadoCafe] [varchar](35) NULL,
 CONSTRAINT [PK_tblEstadoCafe] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblEstadoInvenCafe]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblEstadoInvenCafe](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[EstadoInvenCafe] [varchar](50) NULL,
 CONSTRAINT [PK_tblEstadoInvenCafe] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblEstadoOrdenes]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblEstadoOrdenes](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[EstadoOrden] [varchar](50) NULL,
 CONSTRAINT [PK_tblEstadoOrdenes] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblEstadosClientes]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblEstadosClientes](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[EstadoCliente] [varchar](35) NULL,
 CONSTRAINT [PK_tblEstadosClientes] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblEstadoTareas]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblEstadoTareas](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[EstadoTareas] [varchar](50) NULL,
 CONSTRAINT [PK_tblEstadoTareas] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblInventarioCafe]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblInventarioCafe](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[IdClientes] [int] NULL,
	[IdEstadoCafe] [int] NULL,
	[IdProcesoInvenCafe] [int] NULL,
	[IdVariendadInvenCafe] [int] NULL,
	[IdOrigen] [int] NULL,
	[IdEmpaque] [int] NULL,
	[FechaIngreso] [datetime] NULL,
	[Codigo] [varchar](20) NULL,
	[Cantidad] [float] NULL,
	[Sacos] [int] NULL,
	[CantidadBolsasEmp] [int] NULL,
	[CantidadPaquetes] [int] NULL,
	[created_at] [datetime2](0) NOT NULL,
	[updated_at] [datetime2](0) NULL,
 CONSTRAINT [PK_tblInventarioCafe] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblLogEventos]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblLogEventos](
	[Id] [bigint] IDENTITY(1,1) NOT NULL,
	[FechaUtc] [datetime2](3) NOT NULL,
	[Tabla] [sysname] NOT NULL,
	[Accion] [char](1) NOT NULL,
	[Clave] [nvarchar](200) NOT NULL,
	[ActorUserId] [int] NULL,
	[ActorUsername] [nvarchar](150) NULL,
	[Source] [nvarchar](50) NULL,
	[CorrelationId] [uniqueidentifier] NULL,
	[Datos] [nvarchar](max) NULL,
	[AppName] [nvarchar](128) NULL,
	[Host] [nvarchar](128) NULL,
	[UsuarioSQL] [sysname] NULL,
 CONSTRAINT [PK_tblLogEventos] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblMateriales]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblMateriales](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[IdClientes] [int] NULL,
	[FechaIngreso] [datetime] NULL,
	[CodigoMaterial] [varchar](20) NULL,
	[Descripcion] [varchar](20) NULL,
	[Cantidad] [int] NULL,
	[Estado] [bit] NULL,
	[created_at] [datetime2](0) NOT NULL,
	[updated_at] [datetime2](0) NULL,
 CONSTRAINT [PK_tblMateriales] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblMolienda]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblMolienda](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[IdEstadoTarea] [int] NULL,
	[IdNivelMolienda] [int] NULL,
	[Fecha] [datetime] NULL,
	[IdOrden] [int] NULL,
	[IdInvenCafe] [int] NULL,
	[PesoMoler] [float] NULL,
	[Notas] [varchar](40) NULL,
	[created_at] [datetime2](0) NOT NULL,
	[updated_at] [datetime2](0) NULL,
 CONSTRAINT [PK_tblMolienda] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblNivelMolienda]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblNivelMolienda](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[NivelMolienta] [varchar](50) NULL,
 CONSTRAINT [PK_tblNivelMolienda] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblNivelTueste]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblNivelTueste](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[NivelTueste] [varchar](50) NULL,
 CONSTRAINT [PK_tblNivelTueste] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblOrdenes]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblOrdenes](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[IdClientes] [int] NULL,
	[IdInvenCafe] [int] NULL,
	[IdEstadoOrden] [int] NULL,
	[FechaIngreso] [datetime] NULL,
	[FechaOrden] [datetime] NULL,
	[FechaEntrega] [datetime] NULL,
	[Notas] [varchar](30) NULL,
	[Trilla] [bit] NULL,
	[SelecCafeVerde] [bit] NULL,
	[Tueste] [bit] NULL,
	[SelecCafeTostado] [bit] NULL,
	[Molienda] [bit] NULL,
	[Empaque] [bit] NULL,
	[ConfTrilla] [bit] NULL,
	[ConfSelVerde] [bit] NULL,
	[ConfTueste] [bit] NULL,
	[ConfSelTostado] [bit] NULL,
	[ConfMolienda] [bit] NULL,
	[ConfEmpaque] [bit] NULL,
	[Prioridad] [int] NULL,
	[created_at] [datetime2](0) NOT NULL,
	[updated_at] [datetime2](0) NULL,
 CONSTRAINT [PK_tblOrdenes] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[TblOrdenesSeleccionVerde]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[TblOrdenesSeleccionVerde](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[IdEstadoTareas] [int] NULL,
	[FechaIngreso] [datetime] NULL,
	[Zaranda] [bit] NULL,
	[Grupo1] [varchar](10) NULL,
	[PesoGrupo1] [float] NULL,
	[Grupo2] [varchar](10) NULL,
	[PesoGrupo2] [float] NULL,
	[Grupo3] [varchar](10) NULL,
	[PesoGrupo3] [float] NULL,
	[Grupo4] [varchar](10) NULL,
	[PesoGrupo4] [float] NULL,
	[Grupo5] [varchar](10) NULL,
	[PesoGrupo5] [float] NULL,
	[PesoGrupoRipio] [float] NULL,
	[Catadora] [bit] NULL,
	[CatacionRipio] [bit] NULL,
	[PesoCatRipio] [float] NULL,
	[CatacionBalsos] [bit] NULL,
	[PesoCatBalsos] [float] NULL,
	[CatacionGrupo1] [bit] NULL,
	[PesoCatGrupo1] [float] NULL,
	[CatacionGrupo2] [bit] NULL,
	[PesoCatGrupo2] [float] NULL,
	[PesoAceptado] [float] NULL,
	[MedirHumedad] [bit] NULL,
	[Humedad] [float] NULL,
	[MedirDensidad] [bit] NULL,
	[Densidad] [float] NULL,
	[created_at] [datetime2](0) NOT NULL,
	[updated_at] [datetime2](0) NULL,
 CONSTRAINT [PK_TblOrdenesSeleccionVerde] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblOrdenesTrilla]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblOrdenesTrilla](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[IdEstadoTareas] [int] NULL,
	[FechaIngreso] [datetime] NULL,
	[IdOrden] [int] NULL,
	[PesoCafeBruto] [float] NULL,
	[PesoCafeVerde] [float] NULL,
	[Rendimiento] [float] NULL,
	[created_at] [datetime2](0) NOT NULL,
	[updated_at] [datetime2](0) NULL,
 CONSTRAINT [PK_tblOrdenesTrilla] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblOrigenCafe]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblOrigenCafe](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[Origen] [nvarchar](80) NOT NULL,
 CONSTRAINT [PK_tblOrigenCafe] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblProcesoInvenCafe]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblProcesoInvenCafe](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[ProcesoInvenCafe] [varchar](50) NULL,
 CONSTRAINT [PK_tblProcesoInvenCafe] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblSeleccionTueste]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblSeleccionTueste](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[IdEstadoTareas] [int] NULL,
	[IdOrden] [int] NULL,
	[IdInventarioCafe] [int] NULL,
	[FechaIngreso] [datetime] NULL,
	[CatLimpieza] [bit] NULL,
	[CatQuaker] [bit] NULL,
	[PesoQuaker] [float] NULL,
	[CatGrupo1] [bit] NULL,
	[DescGrupo1] [varchar](20) NULL,
	[PesoGrupo1] [float] NULL,
	[CatGrupo2] [bit] NULL,
	[DescGrupo2] [varchar](20) NULL,
	[PesoGrupo2] [float] NULL,
	[CatGrupo3] [bit] NULL,
	[DescGrupo3] [varchar](20) NULL,
	[PesoGrupo3] [float] NULL,
	[created_at] [datetime2](0) NOT NULL,
	[updated_at] [datetime2](0) NULL,
 CONSTRAINT [PK_tblSeleccionTueste] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblTamanoEmpaque]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblTamanoEmpaque](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[TamanoEmpaque] [varchar](50) NULL,
 CONSTRAINT [PK_tblTamanoEmpaque] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblTipoClientes]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblTipoClientes](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[TipoCliente] [varchar](35) NULL,
	[Estado] [bit] NULL,
 CONSTRAINT [PK_tblTipoClientes] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblTipoIdentificacion]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblTipoIdentificacion](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[TipoIdentificacion] [varchar](50) NULL,
	[Estado] [bit] NULL,
 CONSTRAINT [PK_tblTipoIdentificacion] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblTueste]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblTueste](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[IdOrden] [int] NULL,
	[IdInventarioCafe] [int] NULL,
	[IdEstadoTareas] [int] NULL,
	[IdNivelTueste] [int] NULL,
	[FechaIngreso] [datetime] NULL,
	[Batche] [int] NULL,
	[PesoCafeVede] [float] NULL,
	[PesoCafeTostado] [float] NULL,
	[Rendimiento] [float] NULL,
	[PesoCafeVedeTotal] [float] NULL,
	[PesoCafeTostadoTotal] [float] NULL,
	[Notas] [varchar](40) NULL,
	[NotasOp] [varchar](40) NULL,
	[FechaHoraInicio] [datetime] NULL,
	[ConsumoGas] [float] NULL,
	[ConsumoKWH] [float] NULL,
	[TempDeshidratacion] [float] NULL,
	[TiempoDeshidratacion] [time](7) NULL,
	[Temp1Crack] [float] NULL,
	[Tiempo1Crack] [time](7) NULL,
	[TempFinCurva] [float] NULL,
	[TiempoFinCurva] [time](7) NULL,
	[FechaHoraFin] [datetime] NULL,
	[TempoTueste] [time](7) NULL,
	[TiempoEnfriamiento] [time](7) NULL,
	[created_at] [datetime2](0) NOT NULL,
	[updated_at] [datetime2](0) NULL,
 CONSTRAINT [PK_tblTueste] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblVariedadCafe]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblVariedadCafe](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[VariedadCafe] [varchar](50) NULL,
 CONSTRAINT [PK_tblVariedadCafe] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblVariendadInvenCafe]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblVariendadInvenCafe](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[VariedadInvenCafe] [varchar](50) NULL,
 CONSTRAINT [PK_tblVariendadInvenCafe] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tblZarandaGrupo]    Script Date: 1/09/2025 8:21:20 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblZarandaGrupo](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[ZarandaGrupo] [varchar](50) NULL,
 CONSTRAINT [PK_tblZarandaGrupo] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[tblClientes] ADD  CONSTRAINT [DF_tblClientes_FechaIngreso]  DEFAULT (getdate()) FOR [FechaIngreso]
GO
ALTER TABLE [dbo].[tblClientes] ADD  CONSTRAINT [DF_dbo_tblClientes_created_at]  DEFAULT (sysdatetime()) FOR [created_at]
GO
ALTER TABLE [dbo].[tblCurvasTueste] ADD  CONSTRAINT [DF_tblCurvasTueste_FechaIngreso]  DEFAULT (getdate()) FOR [FechaIngreso]
GO
ALTER TABLE [dbo].[tblEmpaques] ADD  CONSTRAINT [DF_tblEmpaques_FechaIngreso]  DEFAULT (getdate()) FOR [FechaIngreso]
GO
ALTER TABLE [dbo].[tblEmpaques] ADD  CONSTRAINT [DF_dbo_tblEmpaques_created_at]  DEFAULT (sysdatetime()) FOR [created_at]
GO
ALTER TABLE [dbo].[tblInventarioCafe] ADD  CONSTRAINT [DF_tblInventarioCafe_FechaIngreso]  DEFAULT (getdate()) FOR [FechaIngreso]
GO
ALTER TABLE [dbo].[tblInventarioCafe] ADD  CONSTRAINT [DF_dbo_tblInventarioCafe_created_at]  DEFAULT (sysdatetime()) FOR [created_at]
GO
ALTER TABLE [dbo].[tblLogEventos] ADD  CONSTRAINT [DF_tblLogEventos_FechaUtc]  DEFAULT (sysutcdatetime()) FOR [FechaUtc]
GO
ALTER TABLE [dbo].[tblLogEventos] ADD  CONSTRAINT [DF_tblLogEventos_AppName]  DEFAULT (app_name()) FOR [AppName]
GO
ALTER TABLE [dbo].[tblLogEventos] ADD  CONSTRAINT [DF_tblLogEventos_Host]  DEFAULT (host_name()) FOR [Host]
GO
ALTER TABLE [dbo].[tblLogEventos] ADD  CONSTRAINT [DF_tblLogEventos_UsuarioSQL]  DEFAULT (suser_sname()) FOR [UsuarioSQL]
GO
ALTER TABLE [dbo].[tblMateriales] ADD  CONSTRAINT [DF_tblMateriales_FechaIngreso]  DEFAULT (getdate()) FOR [FechaIngreso]
GO
ALTER TABLE [dbo].[tblMateriales] ADD  CONSTRAINT [DF_tblMateriales_Estado]  DEFAULT ((1)) FOR [Estado]
GO
ALTER TABLE [dbo].[tblMateriales] ADD  CONSTRAINT [DF_dbo_tblMateriales_created_at]  DEFAULT (sysdatetime()) FOR [created_at]
GO
ALTER TABLE [dbo].[tblMolienda] ADD  CONSTRAINT [DF_tblMolienda_Fecha]  DEFAULT (getdate()) FOR [Fecha]
GO
ALTER TABLE [dbo].[tblMolienda] ADD  CONSTRAINT [DF_dbo_tblMolienda_created_at]  DEFAULT (sysdatetime()) FOR [created_at]
GO
ALTER TABLE [dbo].[tblOrdenes] ADD  CONSTRAINT [DF_tblOrdenes_FechaIngreso]  DEFAULT (getdate()) FOR [FechaIngreso]
GO
ALTER TABLE [dbo].[tblOrdenes] ADD  CONSTRAINT [DF_dbo_tblOrdenes_created_at]  DEFAULT (sysdatetime()) FOR [created_at]
GO
ALTER TABLE [dbo].[TblOrdenesSeleccionVerde] ADD  CONSTRAINT [DF_TblOrdenesSeleccionVerde_FechaIngreso]  DEFAULT (getdate()) FOR [FechaIngreso]
GO
ALTER TABLE [dbo].[TblOrdenesSeleccionVerde] ADD  CONSTRAINT [DF_dbo_TblOrdenesSeleccionVerde_created_at]  DEFAULT (sysdatetime()) FOR [created_at]
GO
ALTER TABLE [dbo].[tblOrdenesTrilla] ADD  CONSTRAINT [DF_dbo_tblOrdenesTrilla_created_at]  DEFAULT (sysdatetime()) FOR [created_at]
GO
ALTER TABLE [dbo].[tblSeleccionTueste] ADD  CONSTRAINT [DF_tblSeleccionTueste_FechaIngreso]  DEFAULT (getdate()) FOR [FechaIngreso]
GO
ALTER TABLE [dbo].[tblSeleccionTueste] ADD  CONSTRAINT [DF_dbo_tblSeleccionTueste_created_at]  DEFAULT (sysdatetime()) FOR [created_at]
GO
ALTER TABLE [dbo].[tblTipoIdentificacion] ADD  CONSTRAINT [DF_tblTipoIdentificacion_Estado]  DEFAULT ((1)) FOR [Estado]
GO
ALTER TABLE [dbo].[tblTueste] ADD  CONSTRAINT [DF_tblTueste_FechaIngreso]  DEFAULT (getdate()) FOR [FechaIngreso]
GO
ALTER TABLE [dbo].[tblTueste] ADD  CONSTRAINT [DF_dbo_tblTueste_created_at]  DEFAULT (sysdatetime()) FOR [created_at]
GO
ALTER TABLE [dbo].[tblClientes]  WITH CHECK ADD  CONSTRAINT [FK_tblClientes_tblEstadosClientes] FOREIGN KEY([IdEstadoCliente])
REFERENCES [dbo].[tblEstadosClientes] ([Id])
GO
ALTER TABLE [dbo].[tblClientes] CHECK CONSTRAINT [FK_tblClientes_tblEstadosClientes]
GO
ALTER TABLE [dbo].[tblClientes]  WITH CHECK ADD  CONSTRAINT [FK_tblClientes_tblTipoClientes] FOREIGN KEY([IdtipoCliente])
REFERENCES [dbo].[tblTipoClientes] ([Id])
GO
ALTER TABLE [dbo].[tblClientes] CHECK CONSTRAINT [FK_tblClientes_tblTipoClientes]
GO
ALTER TABLE [dbo].[tblClientes]  WITH CHECK ADD  CONSTRAINT [FK_tblClientes_tblTipoIdentificacion] FOREIGN KEY([IdTipoIdentificacion])
REFERENCES [dbo].[tblTipoIdentificacion] ([Id])
GO
ALTER TABLE [dbo].[tblClientes] CHECK CONSTRAINT [FK_tblClientes_tblTipoIdentificacion]
GO
ALTER TABLE [dbo].[tblEmpaques]  WITH CHECK ADD  CONSTRAINT [FK_tblEmpaques_tblCafeEmpaque] FOREIGN KEY([IdOrdenEmpaque])
REFERENCES [dbo].[tblCafeEmpaque] ([Id])
GO
ALTER TABLE [dbo].[tblEmpaques] CHECK CONSTRAINT [FK_tblEmpaques_tblCafeEmpaque]
GO
ALTER TABLE [dbo].[tblEmpaques]  WITH CHECK ADD  CONSTRAINT [FK_tblEmpaques_tblEstadoInvenCafe1] FOREIGN KEY([IdInvenCafe])
REFERENCES [dbo].[tblEstadoInvenCafe] ([Id])
GO
ALTER TABLE [dbo].[tblEmpaques] CHECK CONSTRAINT [FK_tblEmpaques_tblEstadoInvenCafe1]
GO
ALTER TABLE [dbo].[tblEmpaques]  WITH CHECK ADD  CONSTRAINT [FK_tblEmpaques_tblEstadoTareas] FOREIGN KEY([IdEstadoTareas])
REFERENCES [dbo].[tblEstadoTareas] ([Id])
GO
ALTER TABLE [dbo].[tblEmpaques] CHECK CONSTRAINT [FK_tblEmpaques_tblEstadoTareas]
GO
ALTER TABLE [dbo].[tblEmpaques]  WITH CHECK ADD  CONSTRAINT [FK_tblEmpaques_tblOrdenes1] FOREIGN KEY([IdOrden])
REFERENCES [dbo].[tblOrdenes] ([Id])
GO
ALTER TABLE [dbo].[tblEmpaques] CHECK CONSTRAINT [FK_tblEmpaques_tblOrdenes1]
GO
ALTER TABLE [dbo].[tblEmpaques]  WITH CHECK ADD  CONSTRAINT [FK_tblEmpaques_tblTamanoEmpaque] FOREIGN KEY([IdTamano])
REFERENCES [dbo].[tblTamanoEmpaque] ([Id])
GO
ALTER TABLE [dbo].[tblEmpaques] CHECK CONSTRAINT [FK_tblEmpaques_tblTamanoEmpaque]
GO
ALTER TABLE [dbo].[tblInventarioCafe]  WITH CHECK ADD  CONSTRAINT [FK_tblInventarioCafe_tblClientes] FOREIGN KEY([IdClientes])
REFERENCES [dbo].[tblClientes] ([Id])
GO
ALTER TABLE [dbo].[tblInventarioCafe] CHECK CONSTRAINT [FK_tblInventarioCafe_tblClientes]
GO
ALTER TABLE [dbo].[tblInventarioCafe]  WITH CHECK ADD  CONSTRAINT [FK_tblInventarioCafe_tblEmpaques] FOREIGN KEY([IdEmpaque])
REFERENCES [dbo].[tblEmpaques] ([Id])
GO
ALTER TABLE [dbo].[tblInventarioCafe] CHECK CONSTRAINT [FK_tblInventarioCafe_tblEmpaques]
GO
ALTER TABLE [dbo].[tblInventarioCafe]  WITH CHECK ADD  CONSTRAINT [FK_tblInventarioCafe_tblEstadoCafe] FOREIGN KEY([IdEstadoCafe])
REFERENCES [dbo].[tblEstadoCafe] ([id])
GO
ALTER TABLE [dbo].[tblInventarioCafe] CHECK CONSTRAINT [FK_tblInventarioCafe_tblEstadoCafe]
GO
ALTER TABLE [dbo].[tblInventarioCafe]  WITH CHECK ADD  CONSTRAINT [FK_tblInventarioCafe_tblOrigenCafe] FOREIGN KEY([IdOrigen])
REFERENCES [dbo].[tblOrigenCafe] ([Id])
GO
ALTER TABLE [dbo].[tblInventarioCafe] CHECK CONSTRAINT [FK_tblInventarioCafe_tblOrigenCafe]
GO
ALTER TABLE [dbo].[tblInventarioCafe]  WITH CHECK ADD  CONSTRAINT [FK_tblInventarioCafe_tblProcesoInvenCafe] FOREIGN KEY([IdProcesoInvenCafe])
REFERENCES [dbo].[tblProcesoInvenCafe] ([Id])
GO
ALTER TABLE [dbo].[tblInventarioCafe] CHECK CONSTRAINT [FK_tblInventarioCafe_tblProcesoInvenCafe]
GO
ALTER TABLE [dbo].[tblInventarioCafe]  WITH CHECK ADD  CONSTRAINT [FK_tblInventarioCafe_tblVariendadInvenCafe] FOREIGN KEY([IdVariendadInvenCafe])
REFERENCES [dbo].[tblVariendadInvenCafe] ([id])
GO
ALTER TABLE [dbo].[tblInventarioCafe] CHECK CONSTRAINT [FK_tblInventarioCafe_tblVariendadInvenCafe]
GO
ALTER TABLE [dbo].[tblMateriales]  WITH CHECK ADD  CONSTRAINT [FK_tblMateriales_tblClientes] FOREIGN KEY([IdClientes])
REFERENCES [dbo].[tblClientes] ([Id])
GO
ALTER TABLE [dbo].[tblMateriales] CHECK CONSTRAINT [FK_tblMateriales_tblClientes]
GO
ALTER TABLE [dbo].[tblMolienda]  WITH CHECK ADD  CONSTRAINT [FK_tblMolienda_tblEstadoInvenCafe] FOREIGN KEY([IdInvenCafe])
REFERENCES [dbo].[tblEstadoInvenCafe] ([Id])
GO
ALTER TABLE [dbo].[tblMolienda] CHECK CONSTRAINT [FK_tblMolienda_tblEstadoInvenCafe]
GO
ALTER TABLE [dbo].[tblMolienda]  WITH CHECK ADD  CONSTRAINT [FK_tblMolienda_tblEstadoTareas] FOREIGN KEY([IdEstadoTarea])
REFERENCES [dbo].[tblEstadoTareas] ([Id])
GO
ALTER TABLE [dbo].[tblMolienda] CHECK CONSTRAINT [FK_tblMolienda_tblEstadoTareas]
GO
ALTER TABLE [dbo].[tblMolienda]  WITH CHECK ADD  CONSTRAINT [FK_tblMolienda_tblNivelMolienda] FOREIGN KEY([IdNivelMolienda])
REFERENCES [dbo].[tblNivelMolienda] ([Id])
GO
ALTER TABLE [dbo].[tblMolienda] CHECK CONSTRAINT [FK_tblMolienda_tblNivelMolienda]
GO
ALTER TABLE [dbo].[tblMolienda]  WITH CHECK ADD  CONSTRAINT [FK_tblMolienda_tblOrdenes] FOREIGN KEY([IdOrden])
REFERENCES [dbo].[tblOrdenes] ([Id])
GO
ALTER TABLE [dbo].[tblMolienda] CHECK CONSTRAINT [FK_tblMolienda_tblOrdenes]
GO
ALTER TABLE [dbo].[tblOrdenes]  WITH CHECK ADD  CONSTRAINT [FK_tblOrdenes_tblClientes] FOREIGN KEY([IdClientes])
REFERENCES [dbo].[tblClientes] ([Id])
GO
ALTER TABLE [dbo].[tblOrdenes] CHECK CONSTRAINT [FK_tblOrdenes_tblClientes]
GO
ALTER TABLE [dbo].[tblOrdenes]  WITH CHECK ADD  CONSTRAINT [FK_tblOrdenes_tblEstadoInvenCafe] FOREIGN KEY([IdInvenCafe])
REFERENCES [dbo].[tblEstadoInvenCafe] ([Id])
GO
ALTER TABLE [dbo].[tblOrdenes] CHECK CONSTRAINT [FK_tblOrdenes_tblEstadoInvenCafe]
GO
ALTER TABLE [dbo].[tblOrdenes]  WITH CHECK ADD  CONSTRAINT [FK_tblOrdenes_tblEstadoOrdenes] FOREIGN KEY([IdEstadoOrden])
REFERENCES [dbo].[tblEstadoOrdenes] ([Id])
GO
ALTER TABLE [dbo].[tblOrdenes] CHECK CONSTRAINT [FK_tblOrdenes_tblEstadoOrdenes]
GO
ALTER TABLE [dbo].[TblOrdenesSeleccionVerde]  WITH CHECK ADD  CONSTRAINT [FK_TblOrdenesSeleccionVerde_tblEstadoTareas] FOREIGN KEY([IdEstadoTareas])
REFERENCES [dbo].[tblEstadoTareas] ([Id])
GO
ALTER TABLE [dbo].[TblOrdenesSeleccionVerde] CHECK CONSTRAINT [FK_TblOrdenesSeleccionVerde_tblEstadoTareas]
GO
ALTER TABLE [dbo].[tblOrdenesTrilla]  WITH CHECK ADD  CONSTRAINT [FK_tblOrdenesTrilla_tblEstadoTareas] FOREIGN KEY([IdEstadoTareas])
REFERENCES [dbo].[tblEstadoTareas] ([Id])
GO
ALTER TABLE [dbo].[tblOrdenesTrilla] CHECK CONSTRAINT [FK_tblOrdenesTrilla_tblEstadoTareas]
GO
ALTER TABLE [dbo].[tblOrdenesTrilla]  WITH CHECK ADD  CONSTRAINT [FK_tblOrdenesTrilla_tblOrdenes] FOREIGN KEY([IdOrden])
REFERENCES [dbo].[tblOrdenes] ([Id])
GO
ALTER TABLE [dbo].[tblOrdenesTrilla] CHECK CONSTRAINT [FK_tblOrdenesTrilla_tblOrdenes]
GO
ALTER TABLE [dbo].[tblSeleccionTueste]  WITH CHECK ADD  CONSTRAINT [FK_tblSeleccionTueste_tblEstadoTareas] FOREIGN KEY([IdEstadoTareas])
REFERENCES [dbo].[tblEstadoTareas] ([Id])
GO
ALTER TABLE [dbo].[tblSeleccionTueste] CHECK CONSTRAINT [FK_tblSeleccionTueste_tblEstadoTareas]
GO
ALTER TABLE [dbo].[tblSeleccionTueste]  WITH CHECK ADD  CONSTRAINT [FK_tblSeleccionTueste_tblInventarioCafe] FOREIGN KEY([IdInventarioCafe])
REFERENCES [dbo].[tblInventarioCafe] ([Id])
GO
ALTER TABLE [dbo].[tblSeleccionTueste] CHECK CONSTRAINT [FK_tblSeleccionTueste_tblInventarioCafe]
GO
ALTER TABLE [dbo].[tblSeleccionTueste]  WITH CHECK ADD  CONSTRAINT [FK_tblSeleccionTueste_tblOrdenes] FOREIGN KEY([IdOrden])
REFERENCES [dbo].[tblOrdenes] ([Id])
GO
ALTER TABLE [dbo].[tblSeleccionTueste] CHECK CONSTRAINT [FK_tblSeleccionTueste_tblOrdenes]
GO
ALTER TABLE [dbo].[tblTueste]  WITH CHECK ADD  CONSTRAINT [FK_tblTueste_tblEstadoInvenCafe] FOREIGN KEY([IdInventarioCafe])
REFERENCES [dbo].[tblEstadoInvenCafe] ([Id])
GO
ALTER TABLE [dbo].[tblTueste] CHECK CONSTRAINT [FK_tblTueste_tblEstadoInvenCafe]
GO
ALTER TABLE [dbo].[tblTueste]  WITH CHECK ADD  CONSTRAINT [FK_tblTueste_tblEstadoTareas] FOREIGN KEY([IdEstadoTareas])
REFERENCES [dbo].[tblEstadoTareas] ([Id])
GO
ALTER TABLE [dbo].[tblTueste] CHECK CONSTRAINT [FK_tblTueste_tblEstadoTareas]
GO
ALTER TABLE [dbo].[tblTueste]  WITH CHECK ADD  CONSTRAINT [FK_tblTueste_tblInventarioCafe] FOREIGN KEY([IdInventarioCafe])
REFERENCES [dbo].[tblInventarioCafe] ([Id])
GO
ALTER TABLE [dbo].[tblTueste] CHECK CONSTRAINT [FK_tblTueste_tblInventarioCafe]
GO
ALTER TABLE [dbo].[tblTueste]  WITH CHECK ADD  CONSTRAINT [FK_tblTueste_tblNivelTueste] FOREIGN KEY([IdNivelTueste])
REFERENCES [dbo].[tblNivelTueste] ([Id])
GO
ALTER TABLE [dbo].[tblTueste] CHECK CONSTRAINT [FK_tblTueste_tblNivelTueste]
GO
ALTER TABLE [dbo].[tblTueste]  WITH CHECK ADD  CONSTRAINT [FK_tblTueste_tblOrdenes] FOREIGN KEY([IdOrden])
REFERENCES [dbo].[tblOrdenes] ([Id])
GO
ALTER TABLE [dbo].[tblTueste] CHECK CONSTRAINT [FK_tblTueste_tblOrdenes]
GO
ALTER TABLE [dbo].[tblCurvasTueste]  WITH CHECK ADD  CONSTRAINT [CK_tblCurvasTueste_Porcentajes] CHECK  (([PorcentajeAire]>=(0) AND [PorcentajeAire]<=(100) AND ([PorcentajeGas]>=(0) AND [PorcentajeGas]<=(100))))
GO
ALTER TABLE [dbo].[tblCurvasTueste] CHECK CONSTRAINT [CK_tblCurvasTueste_Porcentajes]
GO
ALTER TABLE [dbo].[tblEmpaques]  WITH CHECK ADD  CONSTRAINT [CK_tblEmpaques_cantidades_nonneg] CHECK  ((([CantEmpaque] IS NULL OR [CantEmpaque]>=(0)) AND ([CantEmpacada] IS NULL OR [CantEmpacada]>=(0)) AND ([CantEtiquetas] IS NULL OR [CantEtiquetas]>=(0)) AND ([EmpClientes] IS NULL OR [EmpClientes]>=(0)) AND ([TotalEmpaques] IS NULL OR [TotalEmpaques]>=(0)) AND ([TotalEtiquetas] IS NULL OR [TotalEtiquetas]>=(0)) AND ([TotalPaquetes] IS NULL OR [TotalPaquetes]>=(0))))
GO
ALTER TABLE [dbo].[tblEmpaques] CHECK CONSTRAINT [CK_tblEmpaques_cantidades_nonneg]
GO
ALTER TABLE [dbo].[tblInventarioCafe]  WITH CHECK ADD  CONSTRAINT [CK_tblInventarioCafe_nonneg] CHECK  ((([Cantidad] IS NULL OR [Cantidad]>=(0)) AND ([Sacos] IS NULL OR [Sacos]>=(0)) AND ([CantidadBolsasEmp] IS NULL OR [CantidadBolsasEmp]>=(0)) AND ([CantidadPaquetes] IS NULL OR [CantidadPaquetes]>=(0))))
GO
ALTER TABLE [dbo].[tblInventarioCafe] CHECK CONSTRAINT [CK_tblInventarioCafe_nonneg]
GO
ALTER TABLE [dbo].[tblLogEventos]  WITH CHECK ADD CHECK  (([Datos] IS NULL OR isjson([Datos])=(1)))
GO
ALTER TABLE [dbo].[tblLogEventos]  WITH CHECK ADD  CONSTRAINT [CK_tblLogEventos_Accion] CHECK  (([Accion]='D' OR [Accion]='U' OR [Accion]='I'))
GO
ALTER TABLE [dbo].[tblLogEventos] CHECK CONSTRAINT [CK_tblLogEventos_Accion]
GO
ALTER TABLE [dbo].[tblMolienda]  WITH CHECK ADD  CONSTRAINT [CK_tblMolienda_PesoMoler_nonneg] CHECK  (([PesoMoler] IS NULL OR [PesoMoler]>=(0)))
GO
ALTER TABLE [dbo].[tblMolienda] CHECK CONSTRAINT [CK_tblMolienda_PesoMoler_nonneg]
GO
ALTER TABLE [dbo].[tblOrdenes]  WITH CHECK ADD  CONSTRAINT [CK_tblOrdenes_Fechas] CHECK  (([FechaOrden] IS NULL OR [FechaEntrega] IS NULL OR [FechaEntrega]>=[FechaOrden]))
GO
ALTER TABLE [dbo].[tblOrdenes] CHECK CONSTRAINT [CK_tblOrdenes_Fechas]
GO
ALTER TABLE [dbo].[tblOrdenes]  WITH CHECK ADD  CONSTRAINT [CK_tblOrdenes_Rendimiento_bits] CHECK  ((([Trilla]=(1) OR [Trilla]=(0) OR [Trilla] IS NULL) AND ([SelecCafeVerde]=(1) OR [SelecCafeVerde]=(0) OR [SelecCafeVerde] IS NULL) AND ([Tueste]=(1) OR [Tueste]=(0) OR [Tueste] IS NULL) AND ([SelecCafeTostado]=(1) OR [SelecCafeTostado]=(0) OR [SelecCafeTostado] IS NULL) AND ([Molienda]=(1) OR [Molienda]=(0) OR [Molienda] IS NULL) AND ([Empaque]=(1) OR [Empaque]=(0) OR [Empaque] IS NULL) AND ([ConfTrilla]=(1) OR [ConfTrilla]=(0) OR [ConfTrilla] IS NULL) AND ([ConfSelVerde]=(1) OR [ConfSelVerde]=(0) OR [ConfSelVerde] IS NULL) AND ([ConfTueste]=(1) OR [ConfTueste]=(0) OR [ConfTueste] IS NULL) AND ([ConfSelTostado]=(1) OR [ConfSelTostado]=(0) OR [ConfSelTostado] IS NULL) AND ([ConfMolienda]=(1) OR [ConfMolienda]=(0) OR [ConfMolienda] IS NULL) AND ([ConfEmpaque]=(1) OR [ConfEmpaque]=(0) OR [ConfEmpaque] IS NULL)))
GO
ALTER TABLE [dbo].[tblOrdenes] CHECK CONSTRAINT [CK_tblOrdenes_Rendimiento_bits]
GO
ALTER TABLE [dbo].[TblOrdenesSeleccionVerde]  WITH CHECK ADD  CONSTRAINT [CK_TblOrdenesSeleccionVerde_Humedad] CHECK  (([Humedad] IS NULL OR [Humedad]>=(0) AND [Humedad]<=(100)))
GO
ALTER TABLE [dbo].[TblOrdenesSeleccionVerde] CHECK CONSTRAINT [CK_TblOrdenesSeleccionVerde_Humedad]
GO

/*
	Fix de autoincremento para dbo.tblSeleccionTostado
	Contexto: En algunos entornos, la tabla existe sin columna IDENTITY, provocando
	errores "Cannot insert the value NULL into column 'Id'" al insertar sin especificar 'Id'.
	Solución: Si 'Id' no es IDENTITY, crear una secuencia y agregar un DEFAULT que use
	NEXT VALUE FOR para generar el Id automáticamente. Idempotente y seguro.
*/
IF OBJECT_ID('dbo.tblSeleccionTostado', 'U') IS NOT NULL
AND ISNULL(COLUMNPROPERTY(OBJECT_ID('dbo.tblSeleccionTostado'), 'Id', 'IsIdentity'), 0) <> 1
BEGIN
	DECLARE @start int = 1 + ISNULL((SELECT MAX(Id) FROM dbo.tblSeleccionTostado WITH (HOLDLOCK, TABLOCKX)), 0);

	IF NOT EXISTS (
		SELECT 1 FROM sys.sequences
		WHERE name = 'Seq_tblSeleccionTostado' AND SCHEMA_NAME(schema_id) = 'dbo'
	)
	BEGIN
		DECLARE @sqlCreateSeq nvarchar(400);
		SET @sqlCreateSeq = N'CREATE SEQUENCE dbo.Seq_tblSeleccionTostado AS int START WITH ' + CAST(@start AS nvarchar(20)) + N' INCREMENT BY 1';
		EXEC sp_executesql @sqlCreateSeq;
	END
	ELSE
	BEGIN
		DECLARE @sqlRestartSeq nvarchar(400);
		SET @sqlRestartSeq = N'ALTER SEQUENCE dbo.Seq_tblSeleccionTostado RESTART WITH ' + CAST(@start AS nvarchar(20));
		EXEC sp_executesql @sqlRestartSeq;
	END

	IF NOT EXISTS (
		SELECT 1
		FROM sys.default_constraints dc
		JOIN sys.columns c ON c.default_object_id = dc.object_id
		JOIN sys.tables t ON t.object_id = c.object_id
		WHERE t.name = 'tblSeleccionTostado' AND SCHEMA_NAME(t.schema_id) = 'dbo' AND c.name = 'Id'
	)
	BEGIN
		ALTER TABLE dbo.tblSeleccionTostado
		ADD CONSTRAINT DF_tblSeleccionTostado_Id DEFAULT (NEXT VALUE FOR dbo.Seq_tblSeleccionTostado) FOR Id;
	END
END
GO
