import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { GetUSerDataResponse, LoginResponse } from '../interfaces/responses';
import { BehaviorSubject } from 'rxjs';
import { environment } from '../../environments/environment.development';

@Injectable({
  providedIn: 'root',
})
export class AuthService {

  currentUserLoginOn: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);

  constructor(private http: HttpClient) {
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
    return this.http.post<LoginResponse>(this.API_URL + this.AUTH + '/registro', {
      username,
      password
    });
  }

  getUserData() {
    return this.http.get<GetUSerDataResponse>(this.API_URL + this.USER +'/getUserData');
  }

  setToken(token: string) {
    localStorage.setItem('token', token);
  }

  getToken() {
    return localStorage.getItem('token');
  }

  checkLoginStatus(){
    return !!this.getToken();
  }

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    this.currentUserLoginOn.next(false);
  }
}
