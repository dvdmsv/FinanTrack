import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { GetUSerDataResponse, LoginResponse } from '../interfaces/responses';
import { BehaviorSubject } from 'rxjs';
import { environment } from '../../environments/environment.development';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  currentUserLoginOn: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(
    false
  );

  constructor(private http: HttpClient, private router: Router) {
    this.currentUserLoginOn.next(this.checkLoginStatus());
  }

  private API_URL = environment.API_URL_DOCKER;
  private AUTH = environment.AUTH;
  private USER = environment.USER;

  login(username: string, password: string) {
    return this.http.post<LoginResponse>(this.API_URL + this.AUTH + '/login', {
      username,
      password,
    });
  }

  registro(username: string, password: string) {
    return this.http.post<LoginResponse>(
      this.API_URL + this.AUTH + '/registro',
      {
        username,
        password,
      }
    );
  }

  validToken() {
    return this.http.get(this.API_URL + this.AUTH + '/validToken');
  }

  getUserData() {
    return this.http.get<GetUSerDataResponse>(
      this.API_URL + this.USER + '/getUserData'
    );
  }

  setToken(token: string) {
    localStorage.setItem('token', token);
  }

  getToken() {
    return localStorage.getItem('token');
  }

  checkLoginStatus() {
    return !!this.getToken();
  }

  checkValidToken() {
    // Comprueba si el token es valido
    this.validToken().subscribe({
      error: (err) => {
        return false
      },
    });
  }

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    this.currentUserLoginOn.next(false);
  }
}
