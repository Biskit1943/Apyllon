import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map } from 'rxjs/operators';

import { environment } from '../../environments/environment';
import { Buffer } from 'buffer';
import * as blake2b from 'blake2b';

@Injectable()
export class AuthenticationService {
    constructor(private http: HttpClient) {
    }

    async login(username: string, password: string) {
        const data = new FormData();
        data.append('username', username);
        data.append('password', password);
        const header = {
            headers: new HttpHeaders({
                'enctype': 'application/json'
            })
        };
        try {
            const token = await this.http.post<any>(`${environment.apiUrl}/token`, data, header).toPromise();
            const jwt = token && token.hasOwnProperty('access_token') ? token.access_token : '';
            localStorage.setItem('jwt', jwt);
            const uname = await this.getUsername();
            localStorage.setItem('username', uname);
            const currentUser = {'token': jwt, 'username': uname};
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            return currentUser;
        } catch (err) {
            console.log(err);
        }

    }

    logout() {
        // remove user from local storage to log user out
        localStorage.removeItem('currentUser');
        localStorage.removeItem('jwt');
        localStorage.removeItem('username');
    }

    changePassword(username, newPassword) {
        const data = {'username': username, 'password': newPassword};
        return this.http.put<any>(`${environment.apiUrl}/users/me`, JSON.stringify(data));
    }

    getUsername() {
        return this.http.get(`${environment.apiUrl}/users/me`).pipe(map(user => {
            if (user && user.hasOwnProperty('username')) {
                // @ts-ignore
                return user.username;
            }
        })).toPromise();
    }
}

function hashPwd(pwd) {
    const input = Buffer.from(pwd);
    const proto = blake2b(64);
    proto.update(input);
    return proto.digest('hex');
}
