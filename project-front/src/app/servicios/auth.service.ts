import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { GetUSerDataResponse, LoginResponse } from '../interfaces/responses';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {

  currentUserLoginOn: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);

  constructor(private http: HttpClient) {
    this.currentUserLoginOn.next(this.checkLoginStatus());
  }

  private API_URL = 'http://127.0.0.1:5000';
  
  

  login(username: string, password: string) {
    return this.http.post<LoginResponse>(this.API_URL + '/login', {
      username,
      password,
    });
  }

  registro(username: string, password: string) {
    return this.http.post<LoginResponse>(this.API_URL + '/registro', {
      username,
      password
    });
  }

  getUserData() {
    return this.http.get<GetUSerDataResponse>(this.API_URL + '/getUserData');
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
