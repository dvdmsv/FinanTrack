export interface LoginResponse {
  message: string;
  token: string;
}

export interface UserData {
  exp: number;
  user_id: number;
  username: string;
}

export interface GetUSerDataResponse {
  message: string;
  user_data: UserData;
}

export interface SaldoResponse {
  saldo: number;
}

export interface RegistroPorCategoria {
  categoria: string;
  total_cantidad: number;
  presupuesto: Presupuesto | null;
}

export interface RegistroPorCategoriaResponse {
  categorias: RegistroPorCategoria[];
}

export interface Registro {
  id: number;
  cantidad: number;
  categoria: string;
  concepto: string;
  fecha: string;
  tipo: string
}

export interface RegistroUserResponse {
  registros: Registro[];
}

export interface Categoria {
  es_global: boolean;
  id: number;
  nombre: string;
  user_id: number
}

export interface GetCategoriasResponse {
  categoriasGlobales: Categoria[];
  categoriasUnicas: Categoria[];
}

export interface Presupuesto {
  id: number;
  categoria: string;
  porcentaje: number;
  presupuesto_inicial: number;
  presupuesto_restante: number;
}

export interface GetPresupuestosResponse {
  presupuestos: Presupuesto[];
}

