import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {map} from 'rxjs/operators';

import {environment} from '../../environments/environment';
import {Buffer} from 'buffer';
import * as blake2b from 'blake2b';

@Injectable()
export class AuthenticationService {
  constructor(private http: HttpClient) {
  }

  login(username: string, password: string) {
    const data = new FormData();
    data.append('password', hashPwd(password));
    const header = {
      headers: new HttpHeaders({
        'enctype': 'multipart/form-data'
      })
    };

    return this.http.post<any>(`${environment.apiUrl}/users/${username}/authenticate`, data, header)
      .pipe(map(user => {
        // login successful if there's a jwt token in the response
        if (user && user.token) {
          // store user details and jwt token in local storage to keep user logged in between page refreshes
          localStorage.setItem('currentUser', JSON.stringify(user));
        }

        return user;
      }));
  }

  logout() {
    // remove user from local storage to log user out
    localStorage.removeItem('currentUser');
  }

  changePassword(username, password, newPassword) {
    const data = {username: username, password: hashPwd(password), newPassword: hashPwd(newPassword)};
    return this.http.post<any>(`${environment.apiUrl}/changePassword`, data);
  }
}

function hashPwd(pwd) {
  const input = Buffer.from(pwd);
  const proto = blake2b(64);
  proto.update(input);
  return proto.digest('hex');
}
