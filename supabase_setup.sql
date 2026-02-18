-- ============================================================
-- SETUP SUPABASE - PAULINA MADRID DASHBOARD
-- Ejecutar en: Supabase → SQL Editor → New Query
-- ============================================================

-- Tabla para guardar configuraciones de usuarios
CREATE TABLE IF NOT EXISTS user_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_email TEXT UNIQUE NOT NULL,
    nombre TEXT,
    ajustes JSONB DEFAULT '{}',
    escenario_preferido TEXT DEFAULT 'moderado',
    moneda_preferida TEXT DEFAULT 'EUR',
    descuento_matricula BOOLEAN DEFAULT true,
    inflacion DECIMAL(5,4) DEFAULT 0.03,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla para gastos personalizados
CREATE TABLE IF NOT EXISTS gastos_personalizados (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_email TEXT NOT NULL,
    nombre TEXT NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('mensual', 'anual')),
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_gastos_user ON gastos_personalizados(user_email);
CREATE INDEX IF NOT EXISTS idx_settings_user ON user_settings(user_email);

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para auto-update de updated_at
DROP TRIGGER IF EXISTS update_user_settings_updated_at ON user_settings;
CREATE TRIGGER update_user_settings_updated_at
    BEFORE UPDATE ON user_settings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_gastos_updated_at ON gastos_personalizados;
CREATE TRIGGER update_gastos_updated_at
    BEFORE UPDATE ON gastos_personalizados
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Habilitar RLS (Row Level Security)
ALTER TABLE user_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE gastos_personalizados ENABLE ROW LEVEL SECURITY;

-- Políticas de seguridad: usuarios solo ven sus propios datos
CREATE POLICY "Users can view own settings"
    ON user_settings FOR SELECT
    USING (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can insert own settings"
    ON user_settings FOR INSERT
    WITH CHECK (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can update own settings"
    ON user_settings FOR UPDATE
    USING (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can view own gastos"
    ON gastos_personalizados FOR SELECT
    USING (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can insert own gastos"
    ON gastos_personalizados FOR INSERT
    WITH CHECK (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can update own gastos"
    ON gastos_personalizados FOR UPDATE
    USING (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can delete own gastos"
    ON gastos_personalizados FOR DELETE
    USING (auth.jwt() ->> 'email' = user_email);

-- ============================================================
-- VERIFICACION
-- ============================================================
-- Ejecuta esto para verificar que las tablas se crearon:
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
