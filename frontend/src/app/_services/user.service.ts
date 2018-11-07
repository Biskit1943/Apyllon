import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { User } from '../_models';
import { Buffer } from 'buffer';
import * as blake2b from 'blake2b';
@Injectable()
export class UserService {
  constructor(private http: HttpClient) { }

  getAll() {
    return this.http.get<User[]>(`${environment.apiUrl}/users`);
  }

  getById(id: number) {
    return this.http.get(`${environment.apiUrl}/users/` + id);
  }

  register(user: User) {
    return this.http.post(`${environment.apiUrl}/users`, hashPwd(user));
  }

  update(user: User) {
    return this.http.put(`${environment.apiUrl}/users/` + user.id, hashPwd(user));
  }

  delete(id: number) {
    return this.http.delete(`${environment.apiUrl}/users/` + id);
  }
}

function hashPwd(user: User) {
  const input = Buffer.from(user.password);
  const proto = blake2b(64);
  proto.update(input);
  const h = proto.digest();
  user.password = btoa(String.fromCharCode.apply(null, new Uint8Array(h)));
  return user;
}
