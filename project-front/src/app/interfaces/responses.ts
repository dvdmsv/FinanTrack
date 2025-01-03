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

export interface Presupuesto {
  porcentaje: number | null;
  presupuesto_inicial: number | null;
  presupuesto_restante: number | null;
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
  cantidad: number;
  categoria: string;
  concepto: string;
  fecha: string;
  tipo: string
}

export interface RegistroUserResponse {
  registros: Registro[];
}
